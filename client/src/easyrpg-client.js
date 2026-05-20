
/**
 * https://github.com/ynoproject/ynoserver/blob/master/server/room.go#L267
 * @typedef {'sr' | 'm' | 'tp' | 'jmp' | 'f' | 'spd' | 'spr' | 'fl' | 'rfl' | 'rrfl' | 'tr' | 'h' | 'sys' | 'se' | 'ap' | 'mp' | 'rp' | 'ba' | 'ss' | 'sv' | 'sev' | 'anc'} C2SPacketType
 * these are more scattered but you can do a ctrl+f on "connection.RegisterHandler" in https://github.com/ynoproject/ynoengine/blob/master/src/multiplayer/game_multiplayer.cpp
 * @typedef {'s' | 'ri' | 'ss' | 'sv' | 'ssv' | 'sev' | 'sp' | 'pns' | 'bas' | 'b' | 'c' | 'd' | 'm' | 'jmp' | 'f' | 'spd' | 'spr' | 'fl' | 'rfl' | 'rrfl' | 'tr' | 'h' | 'sys' | 'se' | 'ap' | 'mp' | 'rp' | 'ba' | 'name' | 'cut' | 'cuww'} S2CPacketType
 */

import { checkLocations } from './archipelago-client';
import { handleMapSwitch as checksHandleMapSwitch, processTrigger } from './check';
import { handleSwitch as sessionHandleSwitch, handleMapSwitch as sessionHandleMapSwitch, handleActionEvent as sessionHandleActionEvent } from './dream-session';
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
/** @type Record<string, (function(string): void)[]> */
let switchAborts = {};
/** @type Record<string, (function(number): void)[]> */
let varListeners = {};
/** @type Record<string, (function(string): void)[]> */
let varAborts = {};
/** @type Record<string, (function(): void)[]> */
let eventListeners = {};
/** @type Record<string, (function(string): void)[]> */
let eventAborts = {};
/** @type Record<string, (function(): void)[]> */
let actionEventListeners = {};
/** @type Record<string, (function(string): void)[]> */
let actionEventAborts = {};
/** @type Record<string, (function(): void)[]> */
let pictureListeners = {};
/** @type Record<string, (function(string): void)[]> */
let pictureAborts = {};

let trackedSwitches = new Set();
let trackedVariables = new Set();
let trackedEvents = new Set();
let trackedActionEvents = new Set();
let trackedPictures = new Set();

/**
 * @param {number} swID
 */
export function getCachedSwitch(swID) {
  return switchState[swID] ?? false;
}
/**
 * @param {number} swID 
 * @returns {Promise<boolean>}
 */
export async function getSwitch(swID) {
  if (trackedSwitches.has(swID)) return getCachedSwitch(swID);
  
  sendPacket('ss', [swID, 0]);
  return await waitForSwitchChange(swID);
}

/**
 * @param {number} swID
 * @param {boolean} [alsoFetchCurrentValue]
 */
export function trackSwitch(swID, alsoFetchCurrentValue) {
  trackedSwitches.add(swID);
  sendPacket('ss', [swID, alsoFetchCurrentValue ? 2 : 1]);
}

/**
 * @param {number} swID
 * @returns {Promise<boolean>}
 */
export function waitForSwitchChange(swID) {
  return new Promise((resolve, reject) => {
    switchListeners[swID] ??= [];
    switchListeners[swID].push(resolve);
    switchAborts[swID] ??= [];
    switchAborts[swID].push(reject);
  });
}

/**
 * @param {number} varID
 */
export function getCachedVariable(varID) {
  return varState[varID] ?? 0;
}

/**
 * @param {number} varID
 * @returns {Promise<number>}
 */
export async function getVariable(varID) {
  if (trackedVariables.has(varID)) return getCachedVariable(varID);

  sendPacket('sv', [varID, 0]);
  await waitForVariableChange(varID);

  return getCachedVariable(varID);
}

/**
 * @param {number} varID
 * @param {boolean} [alsoFetchCurrentValue]
 */
export function trackVariable(varID, alsoFetchCurrentValue) {
  trackedSwitches.add(varID);
  sendPacket('sv', [varID, alsoFetchCurrentValue ? 2 : 1]);
}

/**
 * @param {number} varID
 * @returns {Promise<number>}
 */
export function waitForVariableChange(varID) {
  return new Promise((resolve, reject) => {
    varListeners[varID] ??= [];
    varListeners[varID].push(resolve);
    varAborts[varID] ??= [];
    varAborts[varID].push(reject);
  });
}

/**
 * @param {number} evID 
 * @param {boolean} actionEvent
 */
export function trackEvent(evID, actionEvent) {
  const set = actionEvent ? trackedActionEvents : trackedEvents;
  if (set.has(evID)) return;
  set.add(evID);
  sendPacket('sev', [evID, actionEvent ? 1 : 0]);
}
/**
 * @param {number} evID 
 * @param {boolean} actionEvent
 * @returns {Promise<>}
 */
export function waitForEvent(evID, actionEvent) {
  trackEvent(evID, actionEvent);
  const listeners = actionEvent ? actionEventListeners : eventListeners;
  const aborts = actionEvent ? actionEventAborts : eventAborts;
  return new Promise((resolve, reject) => {
    listeners[evID] ??= [];
    // @ts-ignore why do you care
    listeners[evID].push(resolve);
    aborts[evID] ??= [];
    aborts[evID].push(reject);
  });
}

/**
 * @param {string} pictureName 
 */
export function trackPicture(pictureName) {
  if (trackedPictures.has(pictureName)) return;
  trackedPictures.add(pictureName);
  sendPacket('sp', [pictureName]);
}
/**
 * @param {string} pictureName
 * @returns {Promise<>}
 */
export function waitForPicture(pictureName) {
  trackPicture(pictureName);
  return new Promise((resolve, reject) => {
    pictureListeners[pictureName] ??= [];
    // @ts-ignore why do you care
    pictureListeners[pictureName].push(resolve);
    pictureAborts[pictureName] ??= [];
    pictureAborts[pictureName].push(reject);
  });
}

export function getPos() {
  return [x, y];
}

/**
 * @param {number} swID
 * @param {boolean} value
 */
function onSwitch(swID, value) {
  switchState[swID] = value;

  sessionHandleSwitch(swID, value);

  const listeners = switchListeners[swID];
  if (listeners) {
    for (const callback of listeners)
      callback(value);
    listeners.length = 0; 
    switchAborts[swID].length = 0;
  }
}

/**
 * @param {number} varID
 * @param {number} value
 */
function onVariable(varID, value) {
  varState[varID] = value;

  const listeners = varListeners[varID];
  if (listeners) {
    for (const callback of listeners)
      callback(value);
    listeners.length = 0;
    varAborts[varID].length = 0;
  }
}

/**
 * @param {C2SPacketType} type 
 * @param {string[]} args
 * @returns {boolean} don't pass packet along to server
 */
export function onPacket(type, args) {
  if (type === 'ss') {
    onSwitch(parseInt(args[0]), args[1] === '1');
  } else if (type === 'sv') {
    onVariable(parseInt(args[0]), parseInt(args[1]))
  } else if (type === 'm' || type === 'tp' || type === 'jmp') {
    x = parseInt(args[0]);
    y = parseInt(args[1]);
    if (type === 'tp') processTrigger(mapID, 'teleport');
    processTrigger(mapID, 'coords');
  } else if (type === 'sev') {
    const actionEvent = args[1] !== '0';
    const listeners = (actionEvent ? actionEventListeners : eventListeners)[args[0]];
    const aborts = (actionEvent ? actionEventAborts : eventAborts)[args[0]];
    if (actionEvent) sessionHandleActionEvent(parseInt(args[0]));
    if (!listeners) return;
    for (const callback of listeners)
      callback();
    listeners.length = 0;
    aborts.length = 0;
  } else if (type === 'ap') {
    const pictureName = args[16];
    const listeners = pictureListeners[pictureName];
    if (!listeners) return;
    for (const callback of listeners)
      callback();
    listeners.length = 0;
    pictureAborts[pictureName].length = 0;
  } else if (type === 'sr') {
    onNewMap(parseInt(args[0]));
  }
}

function clearListeners(reason) {
  trackedSwitches.clear();
  trackedVariables.clear();
  trackedEvents.clear();
  trackedActionEvents.clear();
  trackedPictures.clear();

  for (const aborts of Object.values(switchAborts)) aborts.forEach(abort => abort(reason));
  switchListeners = {};
  switchAborts = {};
  for (const aborts of Object.values(varAborts)) aborts.forEach(abort => abort(reason));
  varListeners = {};
  varAborts = {};
  for (const aborts of Object.values(eventAborts)) aborts.forEach(abort => abort(reason));
  eventListeners = {};
  eventAborts = {};
  for (const aborts of Object.values(actionEventAborts)) aborts.forEach(abort => abort(reason));
  actionEventListeners = {};
  actionEventAborts = {};
  for (const aborts of Object.values(pictureAborts)) aborts.forEach(abort => abort(reason));
  pictureListeners = {};
  pictureAborts = {};
}

export function onNewMap(newMapID) {
  prevMapID = mapID;
  mapID = newMapID;

  clearListeners('switching room, trackers no longer valid');
  
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