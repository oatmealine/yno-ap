import { client as ap, enabled, slotData } from './client';
import { AWAKE_MAPID, EFFECTS, NEXUS_EVENTS, NEXUS_MAPID } from '../const';
import { getMapID, trackEvent, trackSwitch } from '../easyrpg-client';
import { div, text } from '../lib/html';
import { showToastMessage } from '../ui/toasts';

let sessionIsValid = true;
let usedItems = [];

export function isSessionValid() {
  return sessionIsValid;
}

export function invalidateSession(reason) {
  if (!sessionIsValid) return;

  sessionIsValid = false;
  showToastMessage(`This dream session was invalidated! <b>${text(reason)}</b><br>Wake up to resume check collection.`, 'archipelago', undefined, undefined, true);
  document.querySelector('#ap-session-warning').style.display = 'block';
}

function revalidateSession() {
  if (sessionIsValid) return;

  sessionIsValid = true;
  document.querySelector('#ap-session-warning').style.display = 'none';
}

export function updateSessionValidity() {
  if (!enabled) return;

  const forbiddenItems =
    usedItems.filter(itemName =>
      !ap.items.received.find(item => item.name === itemName)
    );

  if (forbiddenItems.length > 0) {
    invalidateSession(`Used ${forbiddenItems.join(', ')}, which ${forbiddenItems.length === 1 ? 'is' : 'are'} not unlocked.`);
  } else {
    revalidateSession();
  }
}

export function handleMapSwitch(mapID) {
  if (mapID === AWAKE_MAPID) {
    usedItems = [];
    revalidateSession();
    return;
  }

  if (!isSessionValid()) return;

  for (const swID of Object.values(EFFECTS))
    trackSwitch(swID);

  if (mapID === NEXUS_MAPID && slotData.useNexusKeys) {
    for (const evIDs of Object.values(NEXUS_EVENTS))
      for (const evID of Array.isArray(evIDs) ? evIDs : [evIDs])
        trackEvent(evID, true);
  }
}

export function handleSwitch(id, value) {
  if (!isSessionValid()) return;
  for (const [effectName, effectSwitchID] of Object.entries(EFFECTS)) {
    if (effectSwitchID === id && value) {
      usedItems.push(effectName);
    } 
  }
  updateSessionValidity();
}

export function handleActionEvent(id) {
  if (!isSessionValid()) return;

  const mapID = getMapID();

  if (mapID === NEXUS_MAPID && slotData.useNexusKeys) {
    for (const [nexusKey, evIDs] of Object.entries(NEXUS_EVENTS)) {
      for (const evID of Array.isArray(evIDs) ? evIDs : [evIDs]) {
        if (id === evID) {
          usedItems.push(nexusKey);
        }
      }
    }
  }

  updateSessionValidity();
}

export function addWarningElement() {
  const warning = div('#ap-session-warning', 'AP: Dream session invalidated');
  warning.style.position = 'absolute';
  warning.style.fontFamily = 'JF-Dot-Shinonome12';
  warning.style.fontSize = '16px';
  warning.style.color = '#f44';
  warning.style.background = '#000000aa';
  warning.style.padding = '4px';
  warning.classList.add('unselectable');
  
  warning.style.display = 'none';

  document.querySelector('#gameContainer').append(warning);
}

export function updateCanvasOverlays() {
  const warning = document.querySelector('#ap-session-warning');
  const contentElement = document.querySelector('#content');
  const canvasElement = document.querySelector('#canvas');
  
  if (document.fullscreenElement) {
    const canvasRect = canvasElement.getBoundingClientRect();
    warning.style.top = `${canvasRect.y}px`;
    warning.style.left = `${canvasRect.x}px`;
  } else {
    warning.style.top = `${canvasElement.offsetTop - contentElement.scrollTop}px`;
    warning.style.left = `${canvasElement.offsetLeft}px`;
  }
}