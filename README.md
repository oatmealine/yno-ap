# yno-ap

Archipelago world and client implementation for Yume 2kki (and maybe more down
the line?) based on the [YNO Project](https://ynoproject.net/).

## status

Nowhere near playable; you can check the exact specifics of what's there and
what's missing in [TODO.md](./TODO.md). There's a working client that connects
to an Archipelago server, and an apworld that successfully generates, but that's
about it

## how to run

### apworld

Follow standard Archipelago apworld installation instructions. Copy `apworld` in
your Archipelago folder, into `archipelago/worlds/`. Generate a YAML through the
launcher, customize it to your heart's content, then generate a multiworld as
usual.

#### development

My personal preferred way to work on this is by symlinking `apworld` into a
development copy of Archielago cloned directly from the source. You can then
quickly check if the apworld generates with `archipelago/Launcher.py 'Generate'
-- --player_files_path 'archipelago/Players'`.

### client

#### compilation

In the `client` folder (`cd client`), install dependencies (`npm install`), then
build (`npm run build`). You should be left with a `index.user.js` in your
`dist/` folder. Install [Violentmonkey](https://violentmonkey.github.io) (or
euiqvalent), open its dashboard, then drag the script in.

#### development

Follow the same steps as above, except run `npm run dev` instead of `npm run
build` and tick "Track external edits". This'll update the script whenever you
edit any file.

#### use

Switch to the newly-created AP tab in the chat panel. Fill in your details as
needed. **Do note that due to browser security context reasons, you cannot
connect to insecure websockets (ws://).** You can override this in your browser
settings, see:
[Allowing insecure WebSocket connections](https://www.damirscorner.com/blog/posts/20210528-AllowingInsecureWebsocketConnections.html)

## how to play

The YNO implementation has 2 modes of play, decided in the APWorld options:

- On **automatic mode** _(currently unimplemented)_, the client will hook deep
into the game, physically preventing you from doing actions not allowed by your
items. It will also physically give you items whenever you obtain them. This is
the most fluent way to play, and is the "standard" experience.

  Automatic mode should be played on a new save to prevent altering your main
save.

- On **manual mode** _(currently the only implemented mode)_, the client cannot
and will not alter your game state or save. It will only be able to peform basic
checks if you're "cheating" by using items you're not meant to have access to
(effects, etc.). This means that ideally you should play this on a **save that
has every effect**, as this mode will expect you to have the effect in you save
when it is given to you by another location.

  This may be the preferred way to play if you want the Archipelago to act more
like a motivator for you to further your main YNO save's completion.

Modes will not impact logic, but may change filler item behavior.

### location notes

Most effect locations, some events and NPCs are only possible once per save.
Because of this, the code that checks for locations will usually be overly
lenient, in many cases only requiring you to be in the right place, rather than
interacting with the needed object. This prevents softlocks if the client isn't
loaded when the one-time event happens and makes manual mode possible without
save trickery.

## developer documentation

Most documentation about the inner workings of this is stored in the relevant
folders; make sure to check for `readme` files around. Otherwise, feel free to
ask if anything's unclear.

## external links

- [Archipelago server forum thread](https://discord.com/channels/731205301247803413/1483567293886763120)
- [Bluesky post thread (mostly just ramblings)](https://bsky.app/profile/did:plc:7eansezz3nlumwc7gfuiaksv/post/3mgwvokc3k22z)