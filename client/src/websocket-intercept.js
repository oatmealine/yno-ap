import { onPacket, onNewMap } from './easyrpg-client';

const SPLIT_PACKET = '￾';
const SPLIT_ARGS = '￿';
const HEADER_SIZE = 8;

/** @type Set<WebSocket> */
let socketStore = new Set();

/**
 * @param {string} type 
 * @param {string[]} args 
 */
export function sendClientPacket(type, args) {
  sendClientPackets([[type, args]]);
}
/**
 * @param {[string, string[]][]} packets 
 */
export function sendClientPackets(packets) {
  const message = packets.map(([type, args]) => [type, ...args].join(SPLIT_ARGS)).join(SPLIT_PACKET);
  socketStore.forEach(socket => {
    const encoder = new TextEncoder();
    const messageEvent = new MessageEvent('message', {
      data: encoder.encode(message),
      origin: socket.url,
    });
    socket.dispatchEvent(messageEvent);
  });
}

// sendServerPacket is impossible due to ynoguard

function onPacketData(data) {
  let str;
  if (ArrayBuffer.isView(data)) {
    const decoder = new TextDecoder();
    // @ts-ignore
    str = decoder.decode(data.slice(HEADER_SIZE));
  } else if (typeof data === 'string') {
    str = data.slice(HEADER_SIZE);
  } else {
    console.error('[websocket-intercept] idk wtf this is', data);
    return;
  }

  const packets = str
    .split(SPLIT_PACKET)
    .map(packet => packet.split(SPLIT_ARGS));

  // @ts-ignore
  const passthroughPackets = packets.filter(packet => !onPacket(packet[0], packet.slice(1)));

  // we can't actually _only_ filter out the packets we don't care about, bc of
  // ynoguard (signed messages); the most we can do is not respond if there's
  // no non-filtered packets
  if (passthroughPackets.length !== 0)
    return data;

  return null;
}

function isRelevantURL(url) {
  return typeof url === 'string' && url.includes('/room');
}

export function patchWebsocketClass() {
  // patch initializer to capture room sockets
  window.WebSocket = new Proxy(window.WebSocket, {
    construct: (target, args) => {
      const socket = new target(...args);
      if (isRelevantURL(args[0])) {
        console.log('[websocket-intercept] captured socket', socket.url);
        socketStore.add(socket);
        socket.addEventListener('close', () => {
          socketStore.delete(socket);
          console.log('[websocket-intercept] removed socket', socket.url);
        });
        socket.addEventListener('open', () => {
          const url = new URL(args[0]);
          const mapID = parseInt(url.searchParams.get('id'));
          onNewMap(mapID);
        });
      }
      return socket;
    },
  });
  // patch the send method to capture whatever our client sends
  WebSocket.prototype.send = new Proxy(WebSocket.prototype.send, {
    apply: (target, thisArg, argumentsList) => {
      if (isRelevantURL(thisArg.url)) {
        let newPacket;
        try {
          newPacket = onPacketData(argumentsList[0]);
        } catch(err) {
          console.error('[websocket-intercept] error while handling packet:', err);
        }
        if (newPacket === undefined)
          return target.call(thisArg, ...argumentsList);
        else if (newPacket !== null)
          return target.call(thisArg, newPacket);
        else
          return;
      }
      return target.call(thisArg, ...argumentsList);
    },
  });
}