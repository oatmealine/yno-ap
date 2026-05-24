# Yume 2kki Setup Guide

## 0. Generating a multiworld

If you're generating or hosting a game, you must download and install the
APWorld.

Follow standard Archipelago APWorld installation instructions. Download the
[`.apworld` from the latest release](https://github.com/oatmealine/yno-ap/releases).
Move it to your Archipelago folder, into `archipelago/worlds/`.

## 1. Creating a player YAML options file

You can grab a YAML template from
[the latest release](https://github.com/oatmealine/yno-ap/releases).
Alternatively, you can install the APWorld (see above) and use the "Generate
Template Options" entry in the launcher to create a YAML.

The YAML should have sufficient documentation for each option in the comments.

## 2. Installing the YNO userscript

First, you must install a userscript extension for your browser. The recommended
extension is [Violentmonkey](https://violentmonkey.github.io), but any
equivalent (Tampermonkey, Greasemonkey, ...) will likely work.

Open [yno-ap-client.user.js](https://github.com/oatmealine/yno-ap/releases/latest/download/yno-ap-client.user.js)
in your browser and click "Install". Afterwards, you should see a new "AP" tab
on YNO in the chat panel.

## 3. Connecting and playing

Switch to the newly-created "AP" tab. Fill in your details as
needed. **Do note that due to browser security context reasons, you cannot
connect to insecure websockets (ws://).** You can override this in your browser
settings, see:
[Allowing insecure WebSocket connections](https://www.damirscorner.com/blog/posts/20210528-AllowingInsecureWebsocketConnections.html)