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
connect to insecure websockets (ws://).**

## documentation

Most documentation about the inner workings of this is stored in the relevant
folders; make sure to check for `readme` files around. Otherwise, feel free to
ask if anything's unclear.

## external links

- [Archipelago server forum thread](https://discord.com/channels/731205301247803413/1483567293886763120)
- [Bluesky post thread (mostly just ramblings)](https://bsky.app/profile/did:plc:7eansezz3nlumwc7gfuiaksv/post/3mgwvokc3k22z)