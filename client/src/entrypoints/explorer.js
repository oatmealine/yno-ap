import { loadExplorerClientBridge } from '../explorer/bridge';
import { initUI } from '../explorer/ui';

if (window.top === window.self) {
  console.log('[yno-ap-client] running on standalone 2kki explorer, ignoring');
} else {
  console.log('[yno-ap-client] running on 2kki explorer iframe');
  
  initUI();
  loadExplorerClientBridge();
}