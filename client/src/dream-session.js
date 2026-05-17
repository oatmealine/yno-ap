import { client as ap } from './archipelago-client';
import { trackSwitch } from './easyrpg-client';
import { div, text } from './html';
import { showToastMessage } from './ui';

let sessionIsValid = true;

// a map of effect name -> switch id
const EFFECTS = {
  'Bike': 132,
  'Boy': 123,
  'Chainsaw': 124,
  'Lantern': 125,
  'Fairy': 126,
  'Spacesuit': 127,
  'Glasses': 128,
  'Rainbow': 129,
  'Wolf': 130,
  'Eyeball Bomb': 131,
  'Telephone': 122,
  'Maiko': 133,
  'Twintails': 134,
  'Penguin': 135,
  'Insect': 136,
  'Spring': 137,
  'Invisible': 138,
  'School Boy': 139,
  'Plaster Cast': 140,
  'Stretch': 142,
  'Haniwa': 143,
  'Trombone': 144,
  'Cake': 145,
  'Child': 147,
  'Red Riding Hood': 148,
  'Tissue': 149,
  'Bat': 150,
  'Polygon': 151,
  'Teru Teru Bōzu': 152,
  'Marginal': 153,
  'Drum': 154,
  'Grave': 155,
  'Crossing': 156,
  'Bunny Ears': 157,
  'Dice': 158,
};

export function isSessionValid() {
  return sessionIsValid;
}

export function invalidateSession(reason) {
  if (!sessionIsValid) return;

  //sessionIsValid = false;
  showToastMessage(`This dream session was invalidated! <b>${text(reason)}</b><br>Wake up to resume check collection.`, 'archipelago', undefined, undefined, true);
  //document.querySelector('#ap-session-warning').style.display = 'block';
}

function revalidateSession() {
  if (sessionIsValid) return;

  sessionIsValid = true;
  document.querySelector('#ap-session-warning').style.display = 'none';
}

export function handleMapSwitch(mapID) {
  if (mapID === 2) {
    revalidateSession();
    return;
  }

  if (!isSessionValid()) return;

  for (const swID of Object.values(EFFECTS))
    trackSwitch(swID);
}

export function handleSwitch(id, value) {
  if (!isSessionValid()) return;
  for (const [effectName, effectSwitchID] of Object.entries(EFFECTS)) {
    if (effectSwitchID === id && value) {
      if (!ap.items.received.find(item => item.name === effectName)) {
        invalidateSession(`Used effect ${effectName}, which is not unlocked.`);
      }
    } 
  }
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
  const contentElement = document.getElementById('content');
  const canvasElement = document.getElementById('canvas');
  
  if (document.fullscreenElement) {
    const canvasRect = canvasElement.getBoundingClientRect();
    warning.style.top = `${canvasRect.y}px`;
    warning.style.left = `${canvasRect.x}px`;
  } else {
    warning.style.top = `${canvasElement.offsetTop - contentElement.scrollTop}px`;
    warning.style.left = `${canvasElement.offsetLeft}px`;
  }
}