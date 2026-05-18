let slotStoreRoomName = null;
let slotStoreSlotName = null;
export const slotStore = {
  /** @type string[] */
  locationQueue: [],
  /** @type string[] */
  completedConditions: [],
  /** @type string[] */
  completedEndings: [],
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
  /** @type {import("archipelago.js").DataPackage?} */
  dataPackage: { games: {} },
};
const defaultGlobalStore = JSON.parse(JSON.stringify(globalStore));

function mergeIn(base, add) {
  for (let [key, value] of Object.entries(add)) {
    if (
      typeof base[key] === 'object' &&
      typeof value === 'object' &&
      !Array.isArray(base[key]) &&
      !Array.isArray(value) &&
      base[key] !== null &&
      value !== null
    ) {
      mergeIn(base[key], value);
    } else {
      base[key] = value;
    }
  }
}
function mergeInStrict(base, add) {
  for (const key of Object.keys(base)) {
    if (!add[key])
      continue;
    if (typeof base[key] !== typeof add[key])
      continue;

    if (typeof base[key] !== 'object' || Array.isArray(base[key])) {
      base[key] = add[key];
      continue;
    }
      
    mergeIn(base[key], add[key]);
  }
}

function clear(obj) {
  for (let key of Object.keys(obj))
    delete obj[key];
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
  clear(slotStore);
  mergeIn(slotStore, defaultSlotStore);

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

  mergeInStrict(slotStore, parsed);
}

const GLOBAL_STORE_KEY = 'yno-ap-global';

export function saveGlobal() {
  window.localStorage.setItem(GLOBAL_STORE_KEY, JSON.stringify(globalStore));
}
function loadGlobal() {
  clear(slotStore);
  mergeIn(globalStore, defaultGlobalStore);

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

  mergeInStrict(globalStore, parsed);
}
loadGlobal();

window.addEventListener('beforeunload', () => {
  saveGlobal();
  saveSlot();
});