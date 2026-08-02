import { Client, Item, itemsHandlingFlags, PlayerMessageNode } from 'archipelago.js';
import { globalStore, loadSlot, saveGlobal, saveSlot, slotStore } from '../lib/store';
import { updateLocationCompletions } from './check';
import { updateSessionValidity } from './dream-session';
import { GAME_NAME } from '../const';
import { hideStatus, setConnected, setConnecting, updateItemDisplay } from '../ui/status';
import { onToastMessage, showToastMessage } from '../ui/toasts';
import { onMessage } from '../ui/ap-tab';

export const client = new Client();

// whether location checking and item checking should take place as usual
//
// does not indicate whether or not the client is connected; any locations sent
// while connected but not enabled will be queued
export let enabled = false;

client.options.maximumMessages = 0;

// enums ported over from Options.py

/** @enum {number} */
export const ClientMode = Object.freeze({
  Automatic: 1,
  Manual: 2,
});

/** @enum {number} */
export const Goal = Object.freeze({
  AnyEnding: 1,
  AllEndings: 2,
});

/** @enum {number} */
export const AuthorGating = Object.freeze({
  Disable: 1,
  PrimaryAuthor: 2,
  ContributingAuthors: 3,
});

/** @enum {number} */
export const KuraPuzzlesanity = Object.freeze({
  Ignore: 1,
  Unlocking: 2,
  Solving: 3,
});

export const slotData = {
  /** @type {ClientMode} */
  mode: ClientMode.Automatic,
  endings: [ 'Ending #-1', 'Ending #?', 'Ending #1', 'Ending #2', 'Ending #3' ],
  /** @type {Goal} */
  goal: Goal.AllEndings,
  useNexusKeys: false,
  /** @type {AuthorGating} */
  authorGating: AuthorGating.Disable,
  textEvents: false,
  /** @type {KuraPuzzlesanity} */
  kuraPuzzlesanity: KuraPuzzlesanity.Unlocking,
};

/** @type {import('archipelago.js').PackageMetadata?} */
export let pkg;

export async function connect(host, password, slot) {
  if (globalStore.dataPackage)
    client.package.importPackage(globalStore.dataPackage);
  
  setConnecting();

  const remoteSlotData = await client.login(host, slot, GAME_NAME, {
    password,
    items: itemsHandlingFlags.all,
    tags: [ 'Client' ],
    slotData: true,
  });
  
  loadSlot(client.room.seedName, slot);
  console.log('[yno-ap-client] loaded slot store: ', slotStore);

  await client.package.fetchPackage([client.game], true);
  pkg = client.package.findPackage(client.game);

  globalStore.dataPackage = client.package.exportPackage();
  saveGlobal();
  
  enabled = true;

  checkLocationsRaw(...slotStore.locationQueue);
  slotStore.locationQueue = [];
  saveSlot();

  if (remoteSlotData.client_mode !== undefined)
    // @ts-ignore
    slotData.mode = remoteSlotData.client_mode;
  if (remoteSlotData.endings !== undefined)
    // @ts-ignore
    slotData.endings = remoteSlotData.endings;
  if (remoteSlotData.goal !== undefined)
    // @ts-ignore
    slotData.goal = remoteSlotData.goal;
  if (remoteSlotData.use_nexus_keys !== undefined)
    // @ts-ignore
    slotData.useNexusKeys = remoteSlotData.use_nexus_keys;
  if (remoteSlotData.author_gating !== undefined)
    // @ts-ignore
    slotData.authorGating = remoteSlotData.author_gating
  if (remoteSlotData.text_events !== undefined)
    // @ts-ignore
    slotData.textEvents = remoteSlotData.text_events
  if (remoteSlotData.kura_puzzlesanity !== undefined)
    // @ts-ignore
    slotData.kuraPuzzlesanity = remoteSlotData.kura_puzzlesanity
    
  console.log('[yno-ap-client] loaded slot data: ', slotData);

  updateLocationCompletions();
  updateSessionValidity();
  
  setConnected(true);
  //showToastMessage('Connected to Archipelago server successfully', 'archipelago', false, undefined);
}

let silenceNextDisconnect = false;

export function disconnect(disableChecks = false, silent = false) {
  if (disableChecks) {
    enabled = false;
    hideStatus();
  }

  if (silent) silenceNextDisconnect = true;
  client.socket.disconnect();
  silenceNextDisconnect = false;
}

client.socket.on('disconnected', () => {
  setConnected(false);
  globalStore.lastConnection.autoConnect = false;
  saveGlobal();
  saveSlot();
  
  if (silenceNextDisconnect) {
    silenceNextDisconnect = false;
  } else {
    showToastMessage('Archipelago connection closed', 'archipelago', false, undefined, true); 
  }
});

// hacky
let seen = new Set();
client.messages.on('message', (content, nodes) => {
  if (seen.has(nodes)) {
    seen.delete(nodes);
    return;
  }
  onMessage(nodes);
});

/**
 * @param {import('archipelago.js').MessageNode[]} message 
 * @param {string} author 
 */
function stripAuthor(message, author) {
  let sliced = 0;
  const toSlice = author.length;
  while (sliced < toSlice) {
    const node = message[0];
    if (node.text.length <= (toSlice - sliced)) {
      message.shift();
      sliced += node.text.length;
    } else {
      // @ts-ignore doing stupid class hacks for fun
      node.part.text = node.part.text.slice(toSlice - sliced);
      break;
    }
  }
  return message;
}

client.messages.on('chat', (message, player, nodes) => {
  onMessage(stripAuthor(nodes, player.name + ': '), player.name);
  seen.add(nodes);
});
client.messages.on('serverChat', (message, nodes) => {
  onMessage(stripAuthor(nodes, '[Server]: '), 'Server');
  seen.add(nodes);
});
client.messages.on('connected', (text, player, tags, nodes) => {
  onMessage([
    new PlayerMessageNode(client, { text: player.name }),
    ...stripAuthor(nodes, player.name)
  ]);
  seen.add(nodes);
});
client.messages.on('disconnected', (text, player, nodes) => {
  onMessage([
    new PlayerMessageNode(client, { text: player.name }),
    ...stripAuthor(nodes, player.name)
  ]);
  seen.add(nodes);
});

/*** @param {Item} item */
function onItemReceived(item) {
  updateItemDisplay();
}

client.messages.on('itemSent', (content, item, nodes) => 
  (item.locationGame !== client.game) && (onToastMessage(nodes), onItemReceived(item)));
client.messages.on('itemHinted', (content, item, found, nodes) =>
  (item.locationGame === client.game || item.game === client.game) && onToastMessage(nodes));
client.messages.on('itemCheated', (content, item, nodes) =>
  item.locationGame === client.game && (onToastMessage(nodes), onItemReceived(item)));

export async function sendMessage(content) {
  await client.messages.say(content);
}

export function isLocationChecked(locationName) {
  if (!pkg) return false;
  const id = pkg.locationTable[locationName];
  if (!id) return false;
  return client.room.checkedLocations.includes(id);
}

/**
 * @param {string[]} locationNames
 */
async function checkLocationsRaw(...locationNames) {
  if (!pkg) throw Error('no package loaded?');

  // @ts-ignore checked above
  const ids = locationNames.map(loc => pkg.locationTable[loc]);
  if (ids.length === 0) return;

  client.check(...ids);
}

/**
 * @param {string[]} locationNames
 */
export async function checkLocations(...locationNames) {
  if (!enabled) return;

  if (!client.socket.connected || !pkg) {
    slotStore.locationQueue.push(...locationNames);
    saveSlot();
    return;
  }

  checkLocationsRaw(...locationNames);
}