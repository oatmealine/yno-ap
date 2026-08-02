import { addCSS } from '../lib/html';
import { createAPTab } from './ap-tab';
import { initFormatCSS } from './format';
import { createStatus } from './status';
// @ts-ignore
import css from './ui.css';

export function init() {
  addCSS(css);
  initFormatCSS();
  createAPTab();
  createStatus();
}