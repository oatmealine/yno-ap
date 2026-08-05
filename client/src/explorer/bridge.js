/** @typedef {{ type: 'currentLocations', str: string | null }} ClientToFrameMessage */

import { getMapConditions } from '../ap/check';
import { enabled, isLocationChecked, isLocationHinted, pkg } from '../ap/client';
import { getMapID } from '../easyrpg-client';
import { div, text } from '../lib/html';

/** @param {ClientToFrameMessage} data */
function sendMessageToExplorer(data) {
  /** @type {HTMLIFrameElement} */
  // @ts-ignore
  const explorerFrame = document.querySelector('#explorerFrame');
  if (!explorerFrame.contentWindow) return;

  console.log('[yno-ap-client] sending msg to explorer', data);
  explorerFrame.contentWindow.postMessage(data, 'https://explorer.yume.wiki');
}

export function updateLocationTracker() {
  if (!enabled || !pkg) {
    sendMessageToExplorer({
      type: 'currentLocations',
      str: null,
    });
    return;
  }

  const mapID = getMapID();
  const conds = getMapConditions(mapID);
  const locationsRaw = [...new Set(conds.map(cond => cond.parent))];
  const locations = locationsRaw
    // @ts-ignore
    .filter(loc => pkg.locationTable[loc.name])
    .map(({ name }) => ({
      name,
      hinted: isLocationHinted(name),
      checked: isLocationChecked(name),
    }));
  
  if (locations.length === 0) {
    sendMessageToExplorer({
      type: 'currentLocations',
      str: null,
    });
    return;
  }

  const display = [
    ...locations.filter(loc => loc.hinted && !loc.checked)
      .map(({ name }) => `<b>${text(name)}</b>`),
    ...locations.filter(loc => !loc.hinted && !loc.checked)
      .map(({ name }) => text(name)),
    ...locations.filter(loc => loc.checked)
      .map(({ name }) => `<span class="checked-location">${text(name)}</span>`),
  ].join('\n');

  sendMessageToExplorer({
    type: 'currentLocations',
    str: display,
  });
}

// called on ynoproject.net
export function loadYNOAPClientBridge() {
  const explorerFrame = document.querySelector('#explorerFrame');

  explorerFrame.addEventListener('load', () => {
    updateLocationTracker();
  });
}

// called on explorer.yume.wiki
export function loadExplorerClientBridge() {
  window.addEventListener('message', (event) => {
    if (event.origin !== 'https://ynoproject.net') return;
    
    console.log('[yno-ap-client] iframe: recieved msg', event.data);
  
    /** @type {ClientToFrameMessage} */
    const data = event.data;
  
    if (data.type === 'currentLocations') {
      let overlay = document.querySelector('.ap-overlay');
      if (!overlay) {
        overlay = div('.ap-overlay');
        document.body.append(overlay);
      }

      if (data.str) {
        overlay.classList.remove('hidden');
        overlay.innerHTML = data.str;
      } else {
        overlay.classList.add('hidden');
      }
    }
  });
}