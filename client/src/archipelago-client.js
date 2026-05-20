import { Client, itemsHandlingFlags, PlayerMessageNode, TextualMessageNode } from 'archipelago.js';
import { onMessage, onToastMessage, setConnected, showToastMessage } from './ui';
import { globalStore, loadSlot, saveGlobal, saveSlot, slotStore } from './store';
import { updateLocationCompletions } from './check';
import { updateSessionValidity } from './dream-session';

export const client = new Client();

client.options.maximumMessages = 0;

const GAME_NAME = 'Yume 2kki';

// enums ported over from Options.py

export const ClientMode = {
  Automatic: 1,
  Manual: 2,
}; Object.freeze(ClientMode);

export const Goal = {
  AnyEnding: 1,
  AllEndings: 2,
}; Object.freeze(Goal);

export const slotData = {
  mode: ClientMode.Automatic,
  endings: [ 'Ending #-1', 'Ending #?', 'Ending #1', 'Ending #2', 'Ending #3' ],
  goal: Goal.AllEndings,
  useNexusKeys: false,
};

/** @type {import('archipelago.js').PackageMetadata?} */
let pkg;

export async function connect(host, password, slot) {  
  const remoteSlotData = await client.login(host, slot, GAME_NAME, {
    password,
    items: itemsHandlingFlags.all,
    tags: [ 'Client' ],
    slotData: true,
  });
  
  loadSlot(client.room.seedName, slot);
  console.log('[yno-ap-client] loaded slot store: ', slotStore);

  if (globalStore.dataPackage)
    client.package.importPackage(globalStore.dataPackage);

  await client.package.fetchPackage([client.game], true);
  pkg = client.package.findPackage(client.game);

  globalStore.dataPackage = client.package.exportPackage();
  saveGlobal();
  
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
    
  console.log('[yno-ap-client] loaded slot data: ', slotData);

  updateLocationCompletions();
  updateSessionValidity();
  
  setConnected(true);
  showToastMessage('Connected to Archipelago server successfully', 'archipelago', false, undefined);
}

client.socket.on('disconnected', () => {
  setConnected(false);
  showToastMessage('Archipelago connection closed', 'archipelago', false, undefined);
  globalStore.lastConnection.autoConnect = false;
  saveGlobal();
  saveSlot();
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

client.messages.on('itemSent', (content, item, nodes) => 
  item.locationGame === client.game && onToastMessage(nodes));
client.messages.on('itemHinted', (content, item, found, nodes) =>
  (item.locationGame === client.game || item.game === client.game) && onToastMessage(nodes));
client.messages.on('itemCheated', (content, item, nodes) =>
  item.locationGame === client.game && onToastMessage(nodes));

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
  const ids = locationNames.map(loc => pkg.locationTable[loc]);
  if (ids.length === 0) return;

  client.check(...ids);
}

/**
 * @param {string[]} locationNames
 */
export async function checkLocations(...locationNames) {
  if (!client.socket.connected || !pkg) {
    slotStore.locationQueue.push(...locationNames);
    saveSlot();
    return;
  }

  checkLocationsRaw(...locationNames);
}