import { updateCanvasOverlays as sessionUpdateCanvasOverlays } from '../ap/dream-session';

export function patchUpdateCanvasOverlays() {
  const _updateCanvasOverlays = window.updateCanvasOverlays;
  window.updateCanvasOverlays = () => {
    sessionUpdateCanvasOverlays();
    _updateCanvasOverlays();
  }
}