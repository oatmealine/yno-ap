let slotStoreRoomName = null;
let slotStoreSlotName = null;
export const slotStore = {
  /** @type string[] */
  locationQueue: [],
};
const defaultSlotStore = JSON.parse(JSON.stringify(slotStore));

export const globalStore = {
  lastConnection: {
    /** @type string | null */
    host: '',
    /** @type string | null */
    password: '',
    /** @type string | null */
    slot: '',

    autoConnect: false,
  },
};
const defaultGlobalStore = JSON.parse(JSON.stringify(globalStore));

function mergeInto(o1, o2) {
  for (const key of Object.keys(o1)) {
    if (!o2[key])
      continue;
    if (typeof o1[key] !== typeof o2[key])
      continue;

    if (typeof o1[key] !== 'object' || Array.isArray(o1[key])) {
      o1[key] = o2[key];
      continue;
    }
      
    mergeInto(o1[key], o2[key]);
  }
}

function getSlotStorageName(roomName, slotName) {
  return `yno-ap-slot-${roomName}-${slotName}`;
}

export function saveSlot() {
  if (!slotStoreRoomName || !slotStoreSlotName)
    return;

  window.localStorage.setItem(
    getSlotStorageName(slotStoreRoomName, slotStoreSlotName),
    JSON.stringify(slotStore)
  );
}
export function loadSlot(roomName, slotName) {
  mergeInto(slotStore, defaultSlotStore);

  const storage = window.localStorage.getItem(getSlotStorageName(roomName, slotName));
  slotStoreRoomName = roomName;
  slotStoreSlotName = slotName;

  if (!storage)
    return;
  
  let parsed;
  try {
    parsed = JSON.parse(storage);
  } catch(err) {
    console.error('[yno-ap-client] failed to parse yno-ap slot data (corrupt localstorage?)', err);
    return;
  }

  mergeInto(slotStore, parsed);
}

const GLOBAL_STORE_KEY = 'yno-ap-global';

export function saveGlobal() {
  window.localStorage.setItem(GLOBAL_STORE_KEY, JSON.stringify(globalStore));
}
function loadGlobal() {
  mergeInto(globalStore, defaultGlobalStore);

  const storage = window.localStorage.getItem(GLOBAL_STORE_KEY);

  if (!storage)
    return;

  let parsed;
  try {
    parsed = JSON.parse(storage);
  } catch(err) {
    console.error('[yno-ap-client] failed to parse yno-ap slot data (corrupt localstorage?)', err);
    return;
  }

  mergeInto(globalStore, parsed);
}
loadGlobal();

window.addEventListener('beforeunload', () => {
  saveGlobal();
  saveSlot();
});