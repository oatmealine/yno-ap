/** @typedef {{ 'name': string, 'value': string }} AttributeSet */
/** @typedef {AttributeSet | Node | string} Param */

/** 
 * @param {string} name
 * @param {(Param | undefined)[]} params
 * @returns {Element}
*/
export function elem(name, ...params) {
  /** @type {HTMLElement | undefined} */
  let elem;

  let lastSign = '';
  let lastIndex = 0;
  const iter = (idx, chunk) => {
    const chunkStr = name.slice(lastIndex, idx);
    if (!elem) {
      elem = document.createElement(chunkStr)
    } else {
      if (lastSign === '#') elem.id = chunkStr;
      if (lastSign === '.') elem.classList.add(chunkStr);
    }
    lastIndex = idx + 1;
    lastSign = chunk;
  }

  for (const chunk of name.matchAll(/[\.#]/g))
    iter(chunk.index, chunk[0]);
  iter(name.length);
  
  if (!elem) throw 'Invalid element definition';
  
  for (const param of params) {
    if (param === undefined) continue;
    if (typeof param === 'string' || param instanceof Node)
      elem.append(param);
    else
      elem.setAttribute(param.name, param.value);
  }

  return elem;
}

/**
 * @param {string} name 
 * @param {string} value 
 * @returns {AttributeSet}
 */
export function attr(name, value = '') {
  return { name, value };
}

/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLDivElement}
 */
// @ts-ignore
export const div = (params, ...children) => elem(`div${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLSpanElement}
 */
// @ts-ignore
export const span = (params, ...children) => elem(`span${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLButtonElement}
 */
// @ts-ignore
export const button = (params, ...children) => elem(`button${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLLabelElement}
 */
// @ts-ignore
export const label = (params, ...children) => elem(`label${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLInputElement}
 */
// @ts-ignore
export const input = (params, ...children) => elem(`input${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(AttributeSet | undefined)[]} children
 * @returns {HTMLImageElement}
 */
// @ts-ignore
export const img = (params, ...children) => elem(`img${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLAnchorElement}
 */
// @ts-ignore
export const a = (params, ...children) => elem(`a${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Param | undefined)[]} children
 * @returns {HTMLElement}
 */
// @ts-ignore
export const bdi = (params, ...children) => elem(`bdi${params || ''}`, ...children);

export function raw(html) {
  const e = document.createElement('div');
  e.innerHTML = html;
  return e.childNodes;
}

export function text(html) {
  const e = document.createElement('div');
  e.innerText = html;
  const text = e.innerHTML;
  e.remove();
  return text;
}

/**
 * @param {DOMTokenList} classList
 * @param {string} name
 * @param {boolean} value
 */
export function toggleClass(classList, name, value) {
  if (value)
    classList.add(name);
  else
    classList.remove(name);
}

/** @param {string} css */
export function addCSS(css) {
  document.head.append(elem('style', css));
}