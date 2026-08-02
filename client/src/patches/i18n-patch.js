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
  const _init = window.i18next.init;
  window.i18next.init = (options, callback) => {
    mergeIn(options.resources['en'].translation, addI18N);
    return _init(options, callback);
  };
}