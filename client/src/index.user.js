import { addUIElements, patchI18N } from './ui';
import { patchWebsocketClass } from './websocket-intercept';
import { patchXMLHTTPRequest } from './http-intercept';
import { patchChangeLocation } from './easyrpg-client';
import { addWarningElement, updateCanvasOverlays as sessionUpdateCanvasOverlays } from './dream-session';

/*
  name: 'yno AP client',
  match: [ 'https://ynoproject.net/*' ],
  version: pkg.version,
  grant: 'none',
  runAt: 'document-end',
*/

console.log('[yno-ap-client] hello from yno AP client \\o/');

patchWebsocketClass();
//patchXMLHTTPRequest(); // gives access to 'ssv' packet, but not particularly useful for now

document.addEventListener('DOMContentLoaded', () => {
  patchI18N();
  addUIElements();
  addWarningElement();
});

// this is the easiest way to check for when the actual scripts are done loading...

const observer = new MutationObserver((mutationList, observer) => {
  for (const mutation of mutationList) {
    for (const node of mutation.addedNodes) {
      if (node.nodeName === 'SCRIPT' && node.src?.includes('ynoengine')) {
        console.log('[yno-ap-client] yno scripts done loading');

        patchChangeLocation();

        const _updateCanvasOverlays = window.updateCanvasOverlays;
        window.updateCanvasOverlays = () => {
          sessionUpdateCanvasOverlays();
          _updateCanvasOverlays();
        }

        observer.disconnect();
      }
    }
  }
});
observer.observe(document.body, { childList: true });