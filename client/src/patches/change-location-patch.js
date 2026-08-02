import { onChangeLocation } from '../easyrpg-client';

export function patchChangeLocation() {
  // somehow the most reliable hook point?
  const _addChatMapLocation = window.addChatMapLocation;
  window.addChatMapLocation = (locations) => {
    _addChatMapLocation(locations);
    onChangeLocation(locations);
  };
}
