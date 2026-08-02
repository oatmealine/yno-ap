import { addCSS, bdi, div, elem, span } from '../lib/html';

export function formatPlayer(playerName, noPunct) {
  const player = div('.messageSender.format-label',
    //div('.globalIcon.icon.fillIcon'),
    noPunct ? '' : span('.nameMarker.punct', '['),
    bdi('.nameText', playerName),
    noPunct ? '' : span('.nameMarker.punct', ']'),
  );
  if (noPunct) player.classList.add('noPunct');
  return player;
}

/**
 * @param {import("archipelago.js").MessageNode[]} nodes 
 */
export function formatMessageNodes(nodes) {
  let elems = [];

  for (let node of nodes) {
    if (node.type === 'text' || node.type === 'entrance')
      elems.push(node.text);
    if (node.type === 'player')
      //elems.push(node.text);
      elems.push(formatPlayer(node.text, true));
    if (node.type === 'color') {
      const s = span('.format-label', node.text);
      s.classList.add(`color-${node.color}`);
      elems.push(s);
    }
    if (node.type === 'location') {
      //const locationName = apClient.package.lookupLocationName(apClient.game, node.id);
      elems.push(elem('b', node.text));
    }
    if (node.type === 'item') {
      const s = span('.format-label', node.text);
      s.style.fontWeight = 'bold';
      
      if (node.item.filler)
        s.classList.add('item-filler');
      else if (node.item.progression)
        s.classList.add('item-progression');
      else if (node.item.useful)
        s.classList.add('item-useful');
      else if (node.item.trap)
        s.classList.add('item-trap');

      elems.push(s);
    }
  }

  return elems;
}

// borrowed from yno
function getColorRgb(color) {
  return `${color[0]}, ${color[1]}, ${color[2]}`;
}

// borrowed from yno
function getGradientText(colors, smooth) {
  let lastColor = colors[0];
  let ret = `rgb(${getColorRgb(lastColor)}) 0 `;
  colors.forEach(function (color, c) {
    if (color[0] !== lastColor[0] || color[1] !== lastColor[1] || color[2] !== lastColor[2]) {
      const percent = Math.floor(((c + 1) / colors.length) * 10000) / 100;
      ret += `${percent}%, rgb(${getColorRgb(color)}) `;
      if (!smooth)
        ret += `${percent}% `;
      lastColor = color;
    }
  });
  ret += '100%';
  return ret;
}

function parseHex(hex) {
  const int = parseInt(hex.slice(1), 16);
  const r = (int >> 16) & 255;
  const g = (int >> 8) & 255;
  const b = int & 255;
  return [r, g, b];
}

function lerp(a, b, x) {
  return x * (b - a) + a;
}

function genGradientFrom(color) {
  const rgb = parseHex(color);
  return 'linear-gradient(to bottom, '
    + getGradientText([
      rgb.map(n => lerp(n, 255, 0.3)),
      rgb,
      rgb.map(n => Math.floor(n * 0.7)),
      rgb.map(n => Math.floor(n * 0.6))
    ], true)
    + ')';
}

export function initFormatCSS() {
  addCSS(`
    .ap .item-filler { --base-gradient: ${genGradientFrom('#00EEEE')}; }
    .ap .item-progression { --base-gradient: ${genGradientFrom('#AF99EF')} }
    .ap .item-useful { --base-gradient: ${genGradientFrom('#6D8BE8')} }
    .ap .item-trap { --base-gradient: ${genGradientFrom('#FA8072')} }
    
    .ap .color-bold { font-weight: bold; }
    .ap .color-underline { text-decoration: underline; }
    .ap .color-black { --base-gradient: ${genGradientFrom('#000')} }
    .ap .color-red { --base-gradient: ${genGradientFrom('#f66')} }
    .ap .color-green { --base-gradient: ${genGradientFrom('#6f6')} }
    .ap .color-yellow { --base-gradient: ${genGradientFrom('#ff6')} }
    .ap .color-blue { --base-gradient: ${genGradientFrom('#66f')} }
    .ap .color-magenta { --base-gradient: ${genGradientFrom('#f6f')} }
    .ap .color-cyan { --base-gradient: ${genGradientFrom('#6ff')} }
    .ap .color-white { --base-gradient: ${genGradientFrom('#fff')} }
  `);
}