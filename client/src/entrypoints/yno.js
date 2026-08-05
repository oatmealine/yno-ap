import { connect } from '../ap/client';
import { addWarningElement } from '../ap/dream-session';
import { loadYNOAPClientBridge } from '../explorer/bridge';
import { globalStore, saveGlobal } from '../lib/store';
import { patchChangeLocation } from '../patches/change-location-patch';
import { patchI18N } from '../patches/i18n-patch';
import { patchMessageSend } from '../patches/send-message-patch';
import { patchUpdateCanvasOverlays } from '../patches/update-canvas-overlays';
import { patchWebsocketClass } from '../patches/websocket-intercept';
import { init } from '../ui';

patchWebsocketClass();
//patchXMLHTTPRequest(); // gives access to 'ssv' packet, but not particularly useful for now

document.addEventListener('DOMContentLoaded', () => {
  patchI18N();
  init();
  addWarningElement();
});

async function onYNOLoaded() {
  console.log('[yno-ap-client] yno scripts done loading');
  
  patchChangeLocation();
  patchUpdateCanvasOverlays();
  patchMessageSend();

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

// this is the easiest way to check for when the actual scripts are done loading...

const observer = new MutationObserver(async (mutationList, observer) => {
  for (const mutation of mutationList) {
    for (const node of mutation.addedNodes) {
      // @ts-ignore
      if (node.nodeName === 'SCRIPT' && node.src?.includes('ynoengine')) {
        observer.disconnect();
        onYNOLoaded();
      }
    }
  }
});
observer.observe(document.body, { childList: true });

loadYNOAPClientBridge();