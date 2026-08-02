/** @typedef {{ type: 'currentLocations', str: string }} ClientToFrameMessage */

import { addCSS, div } from './html';
import css from './explorer.css';

// called on explorer.yume.wiki
export function loadExplorerClient() {
  if (window.top === window.self) {
    console.log('[yno-ap-client] running on standalone 2kki explorer, ignoring');
    return;
  }
  
  console.log('[yno-ap-client] running on 2kki explorer iframe');

  window.addEventListener('message', (event) => {
    if (event.origin !== 'https://ynoproject.net') return;
    
    console.log('[yno-ap-client] iframe: recieved msg', event.data);

    /** @type {ClientToFrameMessage} */
    const data = event.data;

    if (data.type === 'currentLocations') {
      document.body.append(div('.ap-overlay', data.str));
    }
  });

  addCSS(css);
}

/** @param {ClientToFrameMessage} data */
function sendMessageToExplorer(data) {
  const explorerFrame = document.querySelector('#explorerFrame');

  console.log('[yno-ap-client] sending msg to explorer', data);
  explorerFrame.contentWindow.postMessage(data, 'https://explorer.yume.wiki');
}

// called on ynoproject.net
export function loadYNOAPClientBridge() {
  const explorerFrame = document.querySelector('#explorerFrame');

  explorerFrame.addEventListener('load', () => {
    sendMessageToExplorer({
      type: 'currentLocations',
      str: 'Hai i\'m bunny',
    });
  });
}