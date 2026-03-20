/** 
 * @param {string} name
 * @param {(Node | string)[]} children
 * @returns {Element}
*/
export function elem(name, ...children) {
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

  elem.append(...children);
  return elem;
}
/**
 * @param {string} params
 * @param {(Element | string)[]} children
 * @returns {HTMLDivElement}
 */
// @ts-ignore
export const div = (params, ...children) => elem(`div${params || ''}`, ...children);
/**
 * @param {string} params
 * @param {(Element | string)[]} children
 * @returns {HTMLSpanElement}
 */
// @ts-ignore
export const span = (params, ...children) => elem(`span${params || ''}`, ...children);

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