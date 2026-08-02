import { span } from '../lib/html';
import { formatMessageNodes } from './format';
import { getSvgIcon } from './icons';

// wrapper for showToastMessage
/**
 * @param {string} message
 * @param {string} [icon]
 * @param {boolean} [iconFill]
 * @param {string} [systemName]
 * @param {boolean} [persist]
 * @returns {HTMLDivElement}
 */
export function showToastMessage(message, icon, iconFill, systemName, persist) {
  const toast = window.showToastMessage(message, undefined, false, systemName, persist);
  // allow our custom css in there
  toast.classList.add('ap');
  // use our own getSvgIcon replacement
  if (icon) {
    toast.prepend(getSvgIcon(icon, iconFill));
  }
  return toast;
}

/**
 * @param {string | import("archipelago.js").MessageNode[]} message 
 */
export function onToastMessage(message) {
  const currentToasts =
    document.querySelectorAll('#toastContainer > .toast.ap').length;

  if (currentToasts >= 10) return;
  if (currentToasts >= 9) {
    showToastMessage('..further toasts omitted..', 'archipelago', undefined, undefined, true);
    return;
  }

  let contents;
  if (typeof message === 'string') {
    contents = span('', message.trim());
  } else {
    contents = span('', ...formatMessageNodes(message));
  }
  showToastMessage(contents.innerHTML, 'archipelago', undefined, undefined, true);
}