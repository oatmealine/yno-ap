import { connect, disconnect } from '../ap/client';
import { attr, bdi, button, div, elem, input, label, raw, span, toggleClass } from '../lib/html';
import { globalStore, saveGlobal } from '../lib/store';
import { formatMessageNodes, formatPlayer } from './format';
import { getSvgIcon } from './icons';

const MESSAGES_LIMIT = 100; // as far as i could push it before lag set in

function pushMessageElem(elem) {
  const messages = document.querySelector('#ap #messages');

  const shouldScroll = Math.abs((messages.scrollHeight - messages.scrollTop) - messages.clientHeight) <= 60;

  messages.append(elem);

  let messageElems = [...messages.querySelectorAll('.messageContainer')];
  while (messageElems.length > MESSAGES_LIMIT)
    // @ts-ignore this cannot be undefined
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
      bdi('.messageTimestamp.infoLabel', `${time.getHours().toString().padStart(2, '0')}:${time.getMinutes().toString().padStart(2, '0')}`),
    ),
    div('.message',
      author ? formatPlayer(author) : '',

      div('.messageContentsWrapper', contents),
    )
  ));
}

function createConnectForm() {
  const connectButton = button('', 'Connect', attr('type', 'button'));
  
  const hostLabel = label('.unselectable', 'Host', attr('for', 'connectHost'));
  const hostInput = input('#connectHost', attr('type', 'text'));
  const hostRow = elem('li.formControlRow',
    hostLabel, hostInput
  );

  const passwordLabel = label('.unselectable', 'Password', attr('for', 'connectPassword'));
  const passwordInput = input('#connectPassword', attr('type', 'password'));
  const passwordRow = elem('li.formControlRow',
    passwordLabel, passwordInput
  );

  const slotLabel = label('.unselectable', 'Slot', attr('for', 'connectSlot'));
  const slotInput = input('#connectSlot', attr('type', 'text'));
  const slotRow = elem('li.formControlRow',
    slotLabel, slotInput
  );

  const errorLabel = elem('li.formControlRow.hidden',
    label('')
  );

  const creds = globalStore.lastConnection;

  if (creds.host)
    hostInput.value = creds.host;
  if (creds.password)
    passwordInput.value = creds.password;
  if (creds.slot)
    slotInput.value = creds.slot;

  connectButton.addEventListener('click', async () => {
    errorLabel.classList.add('hidden');

    creds.host = hostInput.value;
    creds.password = passwordInput.value;
    creds.slot = slotInput.value;

    connectButton.setAttribute('disabled', 'true');
    try {
      await connect(creds.host, creds.password, creds.slot);
      creds.autoConnect = true;
      saveGlobal();
    } catch (err) {
      console.error(err);
      // @ts-ignore
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

export function createAPTab() {
  const chatbox = document.querySelector('#chatbox');
  const chatboxContent = document.querySelector('#chatboxContent');
  const chatboxTabs = document.querySelector('#chatboxTabs');

  const apTab = div('#chatboxTabAP.chatboxTab',
    label('.chatboxTabLabel.unselectable', 'AP'),
    attr('data-tab-section', 'ap')
  );

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
  const timestampButton = button(
    '#messageTimestampsButton.iconButton.toggleButton.offToggleButton.unselectable',
    ...timestampIcon,
    attr('data-i18n', '[title]tooltips.chat.toggleMessageTimestamps'),
    attr('i18n-options', '{"clone":{}}'),
    attr('disabled', 'true')
  );

  timestampButton.addEventListener('click', () => {
    timestampButton.classList.toggle('toggled');
    const toggled = timestampButton.classList.contains('toggled');
    toggleClass(messages.classList, 'hideTimestamps', toggled);
    globalStore.hideChatTimestamps = toggled;
    saveGlobal();
  });

  if (globalStore.hideChatTimestamps) {
    messages.classList.add('hideTimestamps');
    timestampButton.classList.add('toggled');
  }

  /** @type {SVGElement} */
  // @ts-ignore
  const disconnectIcon = getSvgIcon('leave').childNodes[0];
  disconnectIcon.setAttribute('width', '15');
  disconnectIcon.setAttribute('height', '15');
  const disconnectButton = button(
    '#disconnectButton.iconButton.unselectable',
    disconnectIcon,
    attr('data-i18n', '[title]tooltips.ap.disconnect'),
    attr('i18n-options', '{"clone":{}}'),
    attr('disabled', 'true')
  );

  disconnectButton.addEventListener('click', () => {
    disconnect(true, true);
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
}