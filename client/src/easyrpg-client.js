
/**
 * https://github.com/ynoproject/ynoserver/blob/master/server/room.go#L267
 * @typedef {'sr' | 'm' | 'tp' | 'jmp' | 'f' | 'spd' | 'spr' | 'fl' | 'rfl' | 'rrfl' | 'tr' | 'h' | 'sys' | 'se' | 'ap' | 'mp' | 'rp' | 'ba' | 'ss' | 'sv' | 'sev' | 'anc'} C2SPacketType
 * these are more scattered but you can do a ctrl+f on "connection.RegisterHandler" in https://github.com/ynoproject/ynoengine/blob/master/src/multiplayer/game_multiplayer.cpp
 * @typedef {'s' | 'ri' | 'ss' | 'sv' | 'ssv' | 'sev' | 'sp' | 'pns' | 'bas' | 'b' | 'c' | 'd' | 'm' | 'jmp' | 'f' | 'spd' | 'spr' | 'fl' | 'rfl' | 'rrfl' | 'tr' | 'h' | 'sys' | 'se' | 'ap' | 'mp' | 'rp' | 'ba' | 'name' | 'cut' | 'cuww'} S2CPacketType
 */

import { checkLocations } from './archipelago-client';
import { handleMapSwitch as checksHandleMapSwitch, processTrigger } from './check';
import { handleSwitch as sessionHandleSwitch, handleMapSwitch as sessionHandleMapSwitch } from './dream-session';
import { sendClientPackets } from './websocket-intercept';

let prevMapID = 0;
let mapID = 0;
let x = 0;
let y = 0;

/** @type Record<number, boolean> */
let switchState = {};
/** @type Record<number, number> */
let varState = {};

/** @type Record<string, (function(boolean): void)[]> */
let switchListeners = {};
/** @type Record<string, (function(number): void)[]> */
let varListeners = {};
/** @type Record<string, (function(): void)[]> */
let eventListeners = {};
/** @type Record<string, (function(): void)[]> */
let actionEventListeners = {};
/** @type Record<string, (function(): void)[]> */
let pictureListeners = {};

let trackedSwitches = new Set();
let trackedVariables = new Set();
let trackedEvents = new Set();
let trackedActionEvents = new Set();
let trackedPictures = new Set();

export function getCachedSwitch(swID) {
  return switchState[swID] ?? false;
}
/**
 * @param {number} swID 
 * @returns Promise<boolean>
 */
export async function getSwitch(swID) {
  if (trackedSwitches.has(swID)) return getCachedSwitch(swID);
  
  sendPacket('ss', [swID, 0]);
  await waitForSwitchChange(swID);
}

export function trackSwitch(swID, alsoFetchCurrentValue) {
  trackedSwitches.add(swID);
  sendPacket('ss', [swID, alsoFetchCurrentValue ? 2 : 1]);
}

export function waitForSwitchChange(swID) {
  return new Promise(resolve => {
    switchListeners[swID] ??= [];
    switchListeners[swID].push(resolve);
  });
}

export function getCachedVariable(varID) {
  return varState[varID] ?? 0;
}

/**
 * @param {number} varID
 * @returns Promise<number>
 */
export async function getVariable(varID) {
  if (trackedVariables.has(varID)) return getCachedVariable(varID);

  sendPacket('sv', [varID, 0]);
  await waitForVariableChange(varID);
}

export function trackVariable(varID, alsoFetchCurrentValue) {
  trackedSwitches.add(varID);
  sendPacket('sv', [varID, alsoFetchCurrentValue ? 2 : 1]);
}

export function waitForVariableChange(varID) {
  return new Promise(resolve => {
    varListeners[varID] ??= [];
    varListeners[varID].push(resolve);
  });
}

function trackEvent(evID, actionEvent) {
  const set = actionEvent ? trackedActionEvents : trackedEvents;
  if (set.has(evID)) return;
  set.add(evID);
  sendPacket('sev', [actionEvent ? 1 : 0]);
}
export function waitForEvent(evID, actionEvent) {
  trackEvent(evID);
  const listeners = actionEvent ? actionEventListeners : eventListeners;
  return new Promise(resolve => {
    listeners[evID] ??= [];
    // @ts-ignore why do you care
    listeners[evID].push(resolve);
  });
}

function trackPicture(pictureName) {
  if (trackedPictures.has(pictureName)) return;
  trackedPictures.add(pictureName);
  sendPacket('sp', [pictureName]);
}
export function waitForPicture(pictureName) {
  trackPicture(pictureName);
  return new Promise(resolve => {
    pictureListeners[pictureName] ??= [];
    // @ts-ignore why do you care
    pictureListeners[pictureName].push(resolve);
  });
}

export function getPos() {
  return [x, y];
}

function onSwitch(swID, value) {
  switchState[swID] = value;

  const listeners = switchListeners[swID];
  if (listeners) {
    for (const callback of listeners)
      callback(value);
    listeners.length = 0; 
  }

  sessionHandleSwitch(parseInt(swID), value);
}

function onVariable(varID, value) {
  varState[varID] = parseInt(value);

  const listeners = varListeners[varID];
  if (listeners) {
    for (const callback of listeners)
      callback(value);
    listeners.length = 0;
  }
}

/**
 * @param {C2SPacketType} type 
 * @param {string[]} args
 * @returns {boolean} don't pass packet along to server
 */
export function onPacket(type, args) {
  if (type === 'ss') {
    onSwitch(args[0], args[1] === '1');
  } else if (type === 'sv') {
    onVariable(args[0], parseInt(args[1]))
  } else if (type === 'm' || type === 'tp' || type === 'jmp') {
    x = parseInt(args[0]);
    y = parseInt(args[1]);
    if (type === 'tp') processTrigger(mapID, 'teleport');
    processTrigger(mapID, 'coords');
  } else if (type === 'sev') {
    const listeners = (args[1] !== '0' ? actionEventListeners : eventListeners)[args[0]];
    if (!listeners) return;
    for (const callback of listeners)
      callback();
    listeners.length = 0;
  } else if (type === 'ap') {
    const pictureName = args[16];
    const listeners = pictureListeners[pictureName];
    if (!listeners) return;
    for (const callback of listeners)
      callback();
  } else if (type === 'sr') {
    onNewMap(parseInt(args[0]));
  }
}

export function onNewMap(newMapID) {
  prevMapID = mapID;
  mapID = newMapID;

  trackedSwitches.clear();
  trackedVariables.clear();
  trackedEvents.clear();
  trackedActionEvents.clear();
  trackedPictures.clear();
  
  // todo: maybe reject these instead of silently discarding the resolves
  switchListeners = {};
  varListeners = {};
  eventListeners = {};
  actionEventListeners = {};
  pictureListeners = {};
  
  checksHandleMapSwitch(newMapID);
  processTrigger(mapID, 'prevMap', prevMapID.toString());

  sessionHandleMapSwitch(newMapID);
}

/**
 * only used for location locations, since it's easier than manually mapping
 * map IDs to location names
 * @param {({title: string})[]} locations
 */
export function onChangeLocation(locations) {
  checkLocations(...locations.map(loc => loc.title));
}

export function patchChangeLocation() {
  // somehow the most reliable hook point?
  window.addChatMapLocation = new Proxy(window.addChatMapLocation, {
    apply: (target, thisArg, argumentsList) => {
      onChangeLocation(argumentsList[0]);
      target(...argumentsList);
    },
  });
}

/**
 * @param {S2CPacketType} type 
 * @param {(string | number | boolean)[]} args 
 */
function sendPacket(type, args) {
  sendPackets([[type, args]]);
}
/**
 * @param {[string, (string | number | boolean)[]][]} packets 
 */
function sendPackets(packets) {
  sendClientPackets(packets.map(([type, args]) => [type, args.map(arg => arg.toString())]))
}