import { Client, itemsHandlingFlags, PlayerMessageNode, TextualMessageNode } from 'archipelago.js';
import { onMessage, onToastMessage, setConnected, showToastMessage } from './ui';

export const client = new Client();

client.options.maximumMessages = 0;

const GAME_NAME = 'Yume 2kki';

// TODO: more permanent storage
/** @type {string[]} */
let locationQueue = [];

export async function connect(host, password, slot) {  
  await client.login(host, slot, GAME_NAME, {
    password,
    items: itemsHandlingFlags.all,
    tags: [ 'Client' ],
  });
  setConnected(true);
  showToastMessage('Connected to Archipelago server successfully', 'archipelago', false, undefined);
  
  checkLocationsRaw(...locationQueue);
  locationQueue = [];
}

client.socket.on('disconnected', () => {
  setConnected(false);
  showToastMessage('Archipelago connection closed', 'archipelago', false, undefined);
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

/**
 * @param {string[]} locationNames
 */
async function checkLocationsRaw(...locationNames) {
  let pkg = client.package.findPackage(client.game);
  if (!pkg)
    pkg = await client.package.fetchPackage([client.game], true)[client.game];

  const ids = locationNames.map(loc => pkg.locationTable[loc]);
  if (ids.length === 0) return;

  client.check(...ids);
}

/**
 * @param {string[]} locationNames
 */
export async function checkLocations(...locationNames) {
  if (!client.socket.connected) {
    locationQueue.push(...locationNames);
    return;
  }

  checkLocationsRaw(...locationNames);
}