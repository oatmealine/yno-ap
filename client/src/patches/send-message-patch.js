import { sendMessage } from '../ap/client';

export function patchMessageSend() {
  const _chatInputActionFired = window.chatInputActionFired;
  window.chatInputActionFired = async () => {
    const chatbox = document.querySelector('#chatbox');
    if (!chatbox.classList.contains('apChat'))
      return await _chatInputActionFired();
    
    /** @type {HTMLInputElement} */
    // @ts-ignore
    const input = document.querySelector('#chatInput');
    if (input.value.trim() === '')
      return;

    sendMessage(input.value.trim());
    input.value = '';
  };
}