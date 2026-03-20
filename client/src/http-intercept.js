const replacements = {
  '/data/2kki/RPG_RT.ini': (orig) => orig.replace(/GameTitle=.+/, 'GameTitle=Collective Unconscious'),
  '/meta.ini': (orig) => orig.replace(/GameTitle=.+/, 'GameTitle=Collective Unconscious'),
};

export function patchXMLHTTPRequest() {
  XMLHttpRequest = new Proxy(XMLHttpRequest, {
    construct: (target) => {
      return new Proxy(new target(), {
        get: (target, propName, ref) => {
          if (target.replacement) {
            if (propName === 'status')
              return 200;
            if (propName === 'response') {
              const decoder = new TextDecoder();
              const decoded = decoder.decode(target[propName]);

              const response = target.replacement(decoded);

              const encoder = new TextEncoder();
              const encoded = encoder.encode(response);

              return encoded;
            }
          }
          
          let temp = target[propName];
          if (temp instanceof Function)
            temp = temp.bind(target);
          return temp;
        },
        set: (target, prop, val, rec) => {
          return Reflect.set(target, prop, val);
        },
      });
    },
  });
  XMLHttpRequest.prototype.open = new Proxy(XMLHttpRequest.prototype.open, {
    /** @param {XMLHttpRequest} thisArg */
    apply: (target, thisArg, argumentsList) => {
      for (const [path, data] of Object.entries(replacements)) {
        if (argumentsList[1].endsWith(path)) {
          thisArg.replacement = data;
        }
      }

      target.call(thisArg, ...argumentsList);
    },
  });
}