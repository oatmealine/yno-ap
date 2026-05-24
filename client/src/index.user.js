import { addUIElements, patchI18N } from './ui';
import { patchWebsocketClass } from './websocket-intercept';
import { patchXMLHTTPRequest } from './http-intercept';
import { patchChangeLocation } from './easyrpg-client';
import { addWarningElement, updateCanvasOverlays as sessionUpdateCanvasOverlays } from './dream-session';
import { globalStore, saveGlobal } from './store';
import { connect } from './archipelago-client';

console.log('[yno-ap-client] hello from yno AP client \\o/');

patchWebsocketClass();
//patchXMLHTTPRequest(); // gives access to 'ssv' packet, but not particularly useful for now

document.addEventListener('DOMContentLoaded', () => {
  patchI18N();
  addUIElements();
  addWarningElement();
});

// this is the easiest way to check for when the actual scripts are done loading...

const observer = new MutationObserver(async (mutationList, observer) => {
  for (const mutation of mutationList) {
    for (const node of mutation.addedNodes) {
      if (node.nodeName === 'SCRIPT' && node.src?.includes('ynoengine')) {
        observer.disconnect();

        console.log('[yno-ap-client] yno scripts done loading');

        patchChangeLocation();

        const _updateCanvasOverlays = window.updateCanvasOverlays;
        window.updateCanvasOverlays = () => {
          sessionUpdateCanvasOverlays();
          _updateCanvasOverlays();
        }

        if (globalStore.lastConnection.autoConnect) {
          const creds = globalStore.lastConnection;

          try {
            await connect(creds.host, creds.password, creds.slot);
          } catch (err) {
            creds.autoConnect = false;
            saveGlobal();
            console.error(err);
          }
        }
      }
    }
  }
});
observer.observe(document.body, { childList: true });