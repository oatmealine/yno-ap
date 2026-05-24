# yno-ap

Archipelago world and client implementation for Yume 2kki (and maybe more down
the line?) based on the [YNO Project](https://ynoproject.net/).

See the [info page](./apworld/docs/en_Yume_2kki.md) for more information.

## status

Somewhat playable! A minimal config with only effect items and effect NPC
locations is playable to completion. This is far from the full scope of this
implementation, however, so I'd advise against playing it currently unless
you're really eager to test it or are simply not interested in the extra
locations and items.

You can check the exact specifics of what's there and
what's missing in [TODO.md](./TODO.md).

## how to play

See the [setup page](./apworld/docs/setup_en.md).

## development

### apworld

My personal preferred way to work on this is by symlinking `apworld` into a
development copy of Archielago cloned directly from the source. You can then
quickly check if the apworld generates with `archipelago/Launcher.py 'Generate'
-- --player_files_path 'archipelago/Players'`.

### client

Go into `client`, run `npm install` to install the dependencies. Run
`npm run dev`, drag the built file from `dist/` into Violentmonkey and tick
"Track external edits". This'll update the script whenever you edit any file.
_(note: changes in location JSONs are not tracked and require rerunning the
command)_

If you just want to build the file once, you can use `npm run build`.

### developer documentation

Most documentation about the inner workings of this is stored in the relevant
folders; make sure to check for `readme` files around. Otherwise, feel free to
ask if anything's unclear.

### scripts

- `scripts/wrapper_dl.py`: Downloads `wrapper.yume.wiki` data and stores it as a
single JSON. Instructions in script.
- `scripts/validate_locations.mjs`: Validates `client/locations/` locations.
This will parse the JSON, validate the schema, and look for common pitfalls.
Requires `python3` to be in path, as it evaluates `apworld/data/__init__.py` to
get a list of known location names; also requires `zod` (installable with the
provided `package.json`).

## external links

- [Archipelago server forum thread](https://discord.com/channels/731205301247803413/1483567293886763120)
- [Bluesky post thread (mostly just ramblings)](https://bsky.app/profile/did:plc:7eansezz3nlumwc7gfuiaksv/post/3mgwvokc3k22z)