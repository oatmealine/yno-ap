import { client as apClient, connect, disconnect, pkg, slotData } from '../ap/client';
import { EFFECTS, NEXUS_IMAGES, NEXUS_KEYS } from '../const';
import { a, attr, div, elem, img, label, span, toggleClass } from '../lib/html';
import { globalStore, saveGlobal } from '../lib/store';
import { getSvgIcon } from './icons';
import { showToastMessage } from './toasts';

function addGradientDef(id, ...colors) {
  const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
  gradient.id = id;

  gradient.setAttribute('x1', '0%');
  gradient.setAttribute('y1', '0%');
  gradient.setAttribute('x2', '0%');
  gradient.setAttribute('y2', '100%');

  gradient.append(...colors.map((col, i, arr) => {
    const stop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop.setAttribute('stop-color', col);
    stop.setAttribute('offset', (i / (arr.length - 1) * 100) + '%');
    return stop;
  }));

  document.querySelector('#svgDefs').append(gradient);
}

let effectsTooltip = div('.tooltipContent');
let nexusKeysTooltip = div('.tooltipContent');
let textEventsTooltip = div('.tooltipContent');
let authorsTooltip = div('.tooltipContent');

export function createStatus() {
  const onlineInfo = document.querySelector('#onlineInfo');

  const statusIcon = span('#apConnStatusIcon', getSvgIcon('archipelago', true));

  const reconnectIcon = getSvgIcon('reconnect', true);
  reconnectIcon.classList.add('altIcon');
  const reconnectButton = a('#apReconnectButton.iconLink.unselectable', reconnectIcon);
  reconnectButton.setAttribute('data-i18n', '[title]chatbox.reconnect');
  reconnectButton.setAttribute('i18n-options', '{"clone":{}}');

  reconnectButton.addEventListener('click', async () => {
    if (reconnectButton.classList.contains('disabled')) return;
    reconnectButton.classList.add('active', 'disabled');

    if (apClient.socket.connected) {
      disconnect(false, true);
      globalStore.lastConnection.autoConnect = true;
    }

    const creds = globalStore.lastConnection;
    try {
      await connect(creds.host, creds.password, creds.slot);
    } catch (err) {
      creds.autoConnect = false;
      saveGlobal();
      console.error(err);
      // @ts-ignore
      showToastMessage(err.message, 'archipelago', false, undefined);
      reconnectButton.classList.remove('active', 'disabled');
      statusIcon.classList.remove('connecting');
    }
  });

  const effectsIcon = span('#apSlotEffects.apSlotIcon', '✨');
  const nexusKeysIcon = span('#apSlotNexusKeys.apSlotIcon', '🔑');
  const textEventsIcon = span('#apSlotTextEvents.apSlotIcon', '💬');
  const authorsIcon = span('#apSlotAuthors.apSlotIcon', '📃');

  window.addTooltip(effectsIcon, effectsTooltip);
  window.addTooltip(nexusKeysIcon, nexusKeysTooltip, false, false, false, {
    theme: Math.random() < 0.5 ? 'ap_nexus_1' : 'ap_nexus_2',
  });
  window.addTooltip(textEventsIcon, textEventsTooltip);
  window.addTooltip(authorsIcon, authorsTooltip);

  const apStatus = div('#apStatus.info',
    span('#apConnStatus.infoContainer.unselectable',
      span('#apConnStatusLabel', 'AP:'), '\n',
      statusIcon, '\n',
      label('#apConnStatusText.infoText', 'Disconnected'), '\n',
      reconnectButton,
    ),
    span('#apSlotInfo.infoLabel',
      span('#apSlotLabel', globalStore.lastConnection.slot ?? ''),
      div('#apSlotItems.unselectable',
        effectsIcon,
        nexusKeysIcon,
        textEventsIcon,
        authorsIcon,
      ),
    ),
  );

  apStatus.classList.add('hidden');
  onlineInfo.after(apStatus);

  addGradientDef('ap_disconnected', '#b30000', '#800000');
  addGradientDef('ap_connecting', '#b35900', '#804000');
  addGradientDef('ap_connected', '#00b33c', '#00802b');
}

export function updateItemDisplay() {
  //const effects = document.querySelector('#apSlotEffects');
  const nexusKeys = document.querySelector('#apSlotNexusKeys');
  const textEvents = document.querySelector('#apSlotTextEvents');
  const authors = document.querySelector('#apSlotAuthors');

  effectsTooltip.innerHTML = '';
  effectsTooltip.append(
    span('.ap-item-count', `${Object.keys(EFFECTS).filter(effect => apClient.items.received.some(item => item.name === effect)).length}/${Object.keys(EFFECTS).length} Effects`),
    div('.ap-items.ap-effects',
      ...Object.keys(EFFECTS).map(
        effect => span(
          apClient.items.received.some(item => item.name === effect)
            ? '.infoLabel.item'
            : '.infoLabel.item.missing',
          effect
        ),
      )
    )
  );

  toggleClass(nexusKeys.classList, 'hidden', !slotData.useNexusKeys);

  nexusKeysTooltip.innerHTML = '';
  nexusKeysTooltip.append(
    span('.ap-item-count', `${NEXUS_KEYS.filter(key => apClient.items.received.some(item => item.name === key)).length}/${NEXUS_KEYS.filter(k => k).length} Nexus Keys`),
    div('.ap-items.ap-nexus-keys',
      ...NEXUS_KEYS.map(key => {
        if (!key) return div('.item.padding');

        const image = img('', attr('src', NEXUS_IMAGES[key]));

        return div(
          (pkg && !pkg.itemTable[key]) ||
          apClient.items.received.some(item => item.name === key)
            ? '.item'
            : '.item.missing',
            image,
          span('.infoLabel', key),
        );
      })
    )
  );
  
  toggleClass(textEvents.classList, 'hidden', !slotData.textEvents);
  toggleClass(textEvents.classList, 'missing', apClient.items.received.some(item => item.name === 'Text Events'));

  toggleClass(authors.classList, 'hidden', !slotData.authorGating);

  authorsTooltip.innerHTML = '';
  authorsTooltip.append(span('', 'Authors: sorry nothing'));
}

function showStatus() {
  const status = document.querySelector('#apStatus');
  status.classList.remove('hidden');
}

export function hideStatus() {
  const status = document.querySelector('#apStatus');
  status.classList.add('hidden');
}

export function setConnecting() {
  const statusIcon = document.querySelector('#apConnStatusIcon');
  statusIcon.classList.add('connecting');
  const statusText = document.querySelector('#apConnStatusText');
  statusText.innerText = 'Connecting...';
}

export function setConnected(connected) {
  if (connected) {
    showStatus();
    updateItemDisplay();
  }

  const statusIcon = document.querySelector('#apConnStatusIcon');
  statusIcon.classList.remove('connecting');
  if (connected) {
    statusIcon.classList.add('connected');
  } else {
    statusIcon.classList.remove('connected');
  }
  
  const statusText = document.querySelector('#apConnStatusText');
  statusText.innerText = connected ? 'Connected' : 'Disconnected';
  
  const reconnectButton = document.querySelector('#apReconnectButton');
  reconnectButton.classList.remove('active', 'disabled');

  const slotLabel = document.querySelector('#apSlotLabel');
  slotLabel.innerText = apClient.name;

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