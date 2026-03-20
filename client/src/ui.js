import { client as apClient, connect, sendMessage } from './archipelago-client';
import { div, elem, raw, span } from './html';

const icons = {
  archipelago: 'M 9 0.25976562 C 7.5273077 0.25976562 6.2680054 1.1859798 5.7792969 2.4882812 C 7.3183487 3.1695008 8.3945293 4.7121008 8.3945312 6.5 C 8.3945312 6.6956211 8.3823049 6.8906778 8.3574219 7.0800781 C 8.5654857 7.1177491 8.7794939 7.140625 9 7.140625 C 9.2205062 7.140625 9.4345144 7.1177471 9.6425781 7.0800781 C 9.6173461 6.8910235 9.6054687 6.6956211 9.6054688 6.5 C 9.6054688 4.7117551 10.679696 3.1695009 12.21875 2.4882812 C 11.730036 1.1859797 10.472692 0.25976563 9 0.25976562 z M 4.0078125 3.0605469 C 2.1093149 3.0605469 0.56640625 4.6046122 0.56640625 6.5 C 0.56640625 7.1086387 0.72521481 7.6836008 1.0058594 8.1816406 C 1.7911106 7.4433936 2.8472156 6.9902344 4.0078125 6.9902344 C 5.1684087 6.9902344 6.2245135 7.4437394 7.0097656 8.1816406 C 7.094788 8.030259 7.1664245 7.875108 7.2265625 7.7109375 C 7.283246 7.5626659 7.3306726 7.411509 7.3652344 7.2539062 C 7.3997954 7.0963027 7.4258697 6.9325599 7.4355469 6.765625 C 7.4448807 6.6806026 7.4492188 6.5881329 7.4492188 6.5 C 7.4492186 5.1659014 6.6855126 4.0065134 5.5722656 3.4355469 C 5.4239942 3.3598558 5.272042 3.2961042 5.1113281 3.2421875 C 4.9630559 3.188616 4.8079935 3.1505921 4.6503906 3.1191406 C 4.442326 3.0814679 4.2283193 3.0605469 4.0078125 3.0605469 z M 13.992188 3.0605469 C 13.771335 3.0605469 13.55572 3.0814686 13.347656 3.1191406 C 13.190053 3.1505916 13.036944 3.1886172 12.888672 3.2421875 C 12.731067 3.2926495 12.579911 3.3586983 12.431641 3.4375 C 11.318394 4.005356 10.550781 5.1662473 10.550781 6.5 C 10.550781 6.588478 10.554863 6.6806018 10.564453 6.765625 C 10.573753 6.9329056 10.597902 7.0963027 10.632812 7.2539062 C 10.667373 7.4115098 10.71479 7.5626659 10.771484 7.7109375 C 10.831274 7.8747623 10.904866 8.0302583 10.990234 8.1816406 C 11.775489 7.4437387 12.831936 6.9882813 13.992188 6.9882812 C 15.152437 6.9882812 16.20889 7.4437387 16.994141 8.1816406 C 17.274788 7.6832543 17.431641 7.1086388 17.431641 6.5 C 17.431641 4.6046125 15.890686 3.0605469 13.992188 3.0605469 z M 4.0078125 7.9355469 C 3.0615007 7.9355469 2.2034586 8.3160728 1.5820312 8.9375 C 1.4686678 9.0477528 1.3638862 9.1687702 1.2695312 9.2949219 C 1.1717207 9.421074 1.0835033 9.5532622 1.0078125 9.6953125 C 0.72716799 10.190588 0.56640625 10.76325 0.56640625 11.375 C 0.56640625 13.273499 2.1093149 14.816406 4.0078125 14.816406 C 4.2220983 14.816406 4.4298119 14.797426 4.6347656 14.759766 C 4.6188696 14.617719 4.6132812 14.473286 4.6132812 14.328125 C 4.6129356 12.521215 5.7111082 10.965307 7.2753906 10.296875 C 7.205921 10.0857 7.116458 9.8847131 7.0058594 9.6953125 C 6.9301684 9.5532622 6.8419509 9.421074 6.7441406 9.2949219 C 6.6494404 9.1687702 6.5469577 9.0477528 6.4335938 8.9375 C 5.8125124 8.3160728 4.9541234 7.9355469 4.0078125 7.9355469 z M 13.992188 7.9355469 C 13.045877 7.9355469 12.190945 8.3180263 11.566406 8.9394531 C 11.456152 9.0497065 11.351717 9.16877 11.253906 9.2949219 C 11.156096 9.4210739 11.067875 9.5532614 10.992188 9.6953125 C 10.881932 9.8843672 10.794078 10.087307 10.724609 10.298828 C 12.288891 10.967261 13.386719 12.521217 13.386719 14.328125 C 13.386719 14.473286 13.381254 14.617717 13.365234 14.759766 C 13.570188 14.797436 13.777557 14.816406 13.992188 14.816406 C 15.890683 14.816406 17.433594 13.275452 17.433594 11.376953 C 17.433594 10.765204 17.272833 10.190243 16.992188 9.6953125 C 16.916158 9.5563764 16.827123 9.4249799 16.732422 9.2988281 C 16.63461 9.1726763 16.531333 9.0528174 16.417969 8.9394531 C 15.796542 8.3180263 14.938497 7.9355469 13.992188 7.9355469 z M 9 10.886719 C 8.7857149 10.886719 8.5780006 10.905699 8.3730469 10.943359 C 8.215444 10.971699 8.0564745 11.013992 7.9082031 11.064453 C 7.7474892 11.118033 7.5935846 11.184072 7.4453125 11.259766 C 6.3258451 11.827275 5.5585938 12.990917 5.5585938 14.328125 C 5.5585938 14.365795 5.55942 14.407271 5.5625 14.445312 C 5.56558 14.615702 5.5837834 14.7823 5.6152344 14.943359 C 5.6404654 15.100963 5.6819632 15.257977 5.7324219 15.40625 C 6.1865684 16.778021 7.4799569 17.771484 9 17.771484 C 10.520042 17.771484 11.813433 16.778021 12.267578 15.40625 C 12.318058 15.257977 12.359534 15.100963 12.384766 14.943359 C 12.416226 14.779535 12.43441 14.611798 12.4375 14.441406 C 12.4407 14.403736 12.441406 14.365809 12.441406 14.328125 C 12.441062 12.990571 11.674156 11.827275 10.554688 11.259766 C 10.406415 11.184076 10.252508 11.118024 10.091797 11.064453 C 9.9435242 11.013983 9.7845563 10.9717 9.6269531 10.943359 C 9.4219996 10.905689 9.214631 10.886719 9 10.886719 z',
};

// shim of YNO's getSvgIcon, but with our own custom ones aswell
function getSvgIcon(iconId, fill) {
  if (!(iconId in icons))
    return window.getSvgIcon(iconId, fill);
  
  const icon = document.createElement('div');
  icon.classList.add(`${iconId}Icon`, 'icon');
  if (fill)
    icon.classList.add('fillIcon');

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 18 18');
  
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', icons[iconId]);

  svg.appendChild(path);
  icon.appendChild(svg);

  return icon;
}

export function formatPlayer(playerName, noPunct) {
  const player = div('.messageSender.format-label',
    //div('.globalIcon.icon.fillIcon'),
    noPunct ? '' : span('.nameMarker.punct', '['),
    elem('bdi.nameText', playerName),
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

// wrapper for showToastMessage
export function showToastMessage(message, icon, iconFill, systemName, persist) {
  const toast = window.showToastMessage(message, null, null, systemName, persist);
  // allow our custom css in there
  toast.classList.add('ap');
  // use our own getSvgIcon replacement
  if (icon) {
    toast.prepend(getSvgIcon(icon, iconFill));
  }
}

function createConnectForm() {
  const connectButton = elem('button', 'Connect');
  connectButton.setAttribute('type', 'button');

  const hostRow = elem('li.formControlRow',
    elem('label.unselectable', 'Host'),
    elem('input#connectHost')
  );
  hostRow.querySelector('label').setAttribute('for', 'connectHost');
  hostRow.querySelector('input').setAttribute('type', 'text');
  const passwordRow = elem('li.formControlRow',
    elem('label.unselectable', 'Password'),
    elem('input#connectPassword')
  );
  passwordRow.querySelector('label').setAttribute('for', 'connectPassword');
  passwordRow.querySelector('input').setAttribute('type', 'password');
  const slotRow = elem('li.formControlRow',
    elem('label.unselectable', 'Slot'),
    elem('input#connectSlot')
  );
  slotRow.querySelector('label').setAttribute('for', 'connectSlot');
  slotRow.querySelector('input').setAttribute('type', 'text');

  const errorLabel = elem('li.formControlRow.hidden',
    elem('label')
  );

  if (window.localStorage.getItem('yno-ap-credentials')) {
    let creds;
    try {
      creds = JSON.parse(window.localStorage.getItem('yno-ap-credentials'));
    } catch(err) {
      console.error('[yno-ap-client] failed to parse yno-ap-credentials (corrupt localstorage?)', err);
    }
    if (creds) {
      hostRow.querySelector('input').value = creds.host;
      passwordRow.querySelector('input').value = creds.password;
      slotRow.querySelector('input').value = creds.slot;
    }
  }

  connectButton.addEventListener('click', async () => {
    errorLabel.classList.add('hidden');

    const creds = {
      host: hostRow.querySelector('input').value,
      password: passwordRow.querySelector('input').value,
      slot: slotRow.querySelector('input').value,
    };

    window.localStorage.setItem('yno-ap-credentials', JSON.stringify(creds));

    connectButton.setAttribute('disabled', 'true');
    try {
      await connect(creds.host, creds.password, creds.slot);
    } catch (err) {
      console.error(err);
      errorLabel.querySelector('label').innerText = err.message;
      errorLabel.classList.remove('hidden');
    }
    connectButton.removeAttribute('disabled');
  });

  return elem('form#apConnectForm',
    elem('ul.formControls',
      hostRow,
      passwordRow,
      slotRow,
      errorLabel
    ),
    connectButton
  );
}

export function setConnected(connected) {
  const connectPrompt = document.querySelector('#ap #apConnect');
  const messages = document.querySelector('#ap #messages');
  const buttons = document.querySelectorAll('#apButtons button');

  if (connected) {
    messages.classList.remove('hidden');
    connectPrompt.classList.add('hidden');
    buttons.forEach(button => button.removeAttribute('disabled'));
    //pushMessageElem(elem('hr'));
  } else {
    messages.classList.add('hidden');
    connectPrompt.classList.remove('hidden');
    buttons.forEach(button => button.setAttribute('disabled', 'true'));
  }
}

const MESSAGES_LIMIT = 100; // as far as i could push it before lag set in

function pushMessageElem(elem) {
  const messages = document.querySelector('#ap #messages');

  const shouldScroll = Math.abs((messages.scrollHeight - messages.scrollTop) - messages.clientHeight) <= 60;

  messages.append(elem);

  let messageElems = [...messages.querySelectorAll('.messageContainer')];
  while (messageElems.length > MESSAGES_LIMIT)
    messageElems.shift().replaceWith(messageElems[0]);

  // actual yno uses fastdom here, but i cba
  if (shouldScroll)
    messages.scrollTop = messages.scrollHeight;
}

/**
 * @param {string | import("archipelago.js").MessageNode[]} message 
 * @param {string} [author]
 */
export function onMessage(message, author) {
  const time = new Date();

  let contents;
  if (typeof message === 'string') {
    contents = span('.messageContents', message.trim());
  } else {
    contents = span('.messageContents', ...formatMessageNodes(message));
  }

  pushMessageElem(div('.messageContainer',
    div('.messageHeader',
      span(''),
      elem('bdi.messageTimestamp.infoLabel', `${time.getHours().toString().padStart(2, '0')}:${time.getMinutes().toString().padStart(2, '0')}`),
    ),
    div('.message',
      author ? formatPlayer(author) : '',

      div('.messageContentsWrapper', contents),
    )
  ));
}

/**
 * @param {string | import("archipelago.js").MessageNode[]} message 
 */
export function onToastMessage(message) {
  let contents;
  if (typeof message === 'string') {
    contents = span('', message.trim());
  } else {
    contents = span('', ...formatMessageNodes(message));
  }
  showToastMessage(contents.innerHTML, 'archipelago', undefined, undefined, true);
}

function addCSS(css) {
  document.head.append(elem('style', css));
}

function patchMessageSend() {
  document.querySelector('#chatInputContainer > form').addEventListener('submit', () => {
    const chatbox = document.querySelector('#chatbox');
    if (!chatbox.classList.contains('apChat'))
      return;

    sendMessage(document.getElementById('chatInput').value.trim());
    document.getElementById('chatInput').value = '';
  });
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

const addI18N = {
  tooltips: {
    ap: {
      disconnect: 'Disconnect',
    },
  },
};

function mergeIn(base, add) {
  for (let [key, value] of Object.entries(add)) {
    if (typeof base[key] === 'object' && typeof value === 'object') {
      mergeIn(base[key], value);
    } else {
      base[key] = value;
    }
  }
}

export function patchI18N() {
  window.i18next.init = new Proxy(window.i18next.init, {
    apply: (target, thisArg, argumentsList) => {
      const opts = argumentsList[0];
      mergeIn(opts.resources['en'].translation, addI18N);
      return target.call(thisArg, ...argumentsList);
    },
  });
}

export function addUIElements() {
  addCSS(`
    #apConnect {
      padding: 8px;
    }
    #apConnect .formControlRow {
      display: flex;
    }
    #apConnect .formControlRow > label {
      flex: 0 0 auto;
      max-width: 100%;
    }
    #apConnect .formControlRow > input {
      flex: 1 1 0;
      min-width: 0;
    }
    
    #ap #messages .messageWrapper {
      overflow-wrap: break-word;
      word-break: break-all;
    }
    #ap #messages .messageContents {
      white-space: pre-wrap;
    }

    #ap #messages .nameText.server {
      font-weight: bold;
      color: #fff;
    }

    .ap .format-label {
      background-image: var(--base-gradient) !important;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      filter: drop-shadow(1.5px 1.5px rgb(var(--shadow-color)));
    }

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

    .ap .messageContents .messageSender, .ap .toastMessage .messageSender {
      float: unset;
      height: unset;
      padding-inline-end: unset;
      display: inline-block;
    }

    .ap .messageContents .messageSender.noPunct, .ap .toastMessage .messageSender.noPunct {
      --base-gradient: var(--alt-gradient);
    }

    .ap .iconButton[disabled] {
      transform: none !important;
      cursor: default;
      opacity: 0.65;
    }

    .ap #apButtons {
      display: flex;
      gap: 4px;
    }
  `);

  const chatbox = document.querySelector('#chatbox');
  const chatboxContent = document.querySelector('#chatboxContent');
  const chatboxTabs = document.querySelector('#chatboxTabs');

  const apTab = div('#chatboxTabAP.chatboxTab',
    elem('label.chatboxTabLabel.unselectable', 'AP')
  );
  apTab.setAttribute('data-tab-section', 'ap');

  chatboxTabs.append(apTab);

  // pretty hacky. oh well.

  let oldClassName;

  document.querySelectorAll('.chatboxTab').forEach(tab => {
    tab.addEventListener('click', () => {
      if (oldClassName) {
        chatbox.className = oldClassName;
        oldClassName = null;
      }
    });
  })

  apTab.addEventListener('click', () => {
    oldClassName = chatbox.className;
    chatbox.className = 'apChat';
  });

  const connectPrompt = div('#apConnect.chatboxTabContent',
    elem('h1.center', `Archipelago`),
    div('', 'Connect to a game:'),
    createConnectForm()
  );

  const messages = div('#messages.chatboxTabContent.scrollableContainer.hidden');

  // not really a non-hacky way to do this unfortunately
  const timestampIcon = raw(`
    <svg viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" width="15" height="15">
      <path d="m9 0a1 1 0 0 0 0 18 1 1 0 0 0 0-18m0 3v6l4 4"></path><path d="m-2 16l22-14"></path>
    </svg>
  `);
  const timestampButton = elem('button#messageTimestampsButton.iconButton.toggleButton.offToggleButton.unselectable', ...timestampIcon);
  timestampButton.setAttribute('data-i18n', '[title]tooltips.chat.toggleMessageTimestamps');
  timestampButton.setAttribute('i18n-options', '{"clone":{}}');
  timestampButton.setAttribute('disabled', 'true');

  timestampButton.addEventListener('click', () => {
    timestampButton.classList.toggle('toggled');
    const toggled = timestampButton.classList.contains('toggled');
    messages.classList.toggle('hideTimestamps', toggled);
  });

  const disconnectIcon = getSvgIcon('leave').childNodes[0];
  disconnectIcon.setAttribute('width', '15');
  disconnectIcon.setAttribute('height', '15');
  const disconnectButton = elem('button#disconnectButton.iconButton.unselectable', disconnectIcon);
  disconnectButton.setAttribute('data-i18n', '[title]tooltips.ap.disconnect');
  disconnectButton.setAttribute('i18n-options', '{"clone":{}}');
  disconnectButton.setAttribute('disabled', 'true');

  disconnectButton.addEventListener('click', () => {
    apClient.socket.disconnect();
  });

  const apSection = div('#ap.ap.chatboxTabSection.hidden',
    div('#apHeader.tabHeader',
      div('#apTabs.subTabs'),
      div('#apButtons.tabButtons',
        timestampButton,
        disconnectButton,
      )
    ),

    connectPrompt,
    messages,
  );

  chatboxContent.append(apSection);

  patchMessageSend();
}