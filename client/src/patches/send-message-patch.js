import { sendMessage } from '../ap/client';

export function patchMessageSend() {
  document.querySelector('#chatInputContainer > form').addEventListener('submit', () => {
    const chatbox = document.querySelector('#chatbox');
    if (!chatbox.classList.contains('apChat'))
      return;
    /** @type {HTMLInputElement} */
    // @ts-ignore
    const input = document.querySelector('#chatInput');
    if (input.value.trim() === '')
      return;

    sendMessage(input.value.trim());
    input.value = '';
  });
}