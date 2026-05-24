# Yume 2kki

## Where is the options page?

The [player options page for this game](../player-options) contains all the
options you need to configure and export a config file.

## What does randomization do to this game?

The items and locations randomized are heavily customizable in the player
options. As a baseline, effects are randomized, but there are also additional
options for turning menu themes, NPCs, events, wallpapers, Kura Puzzles, VMs,
and even just visiting worlds into locations.

To outbalance the locations, there are several item-gating options aswell, which
are recommended if you're not playing in a multiworld where another slot is
extremely item-heavy. Access to Nexus worlds, worlds created by certain authors
and text events can be turned into items to help with the balance.

The filler items of this world don't do anything special, as YNO does not give
much in the ways of being able to control the client. However, this is not the
case on automatic mode, which will give money, wallpapers, menu themes and so on
as filler items. Though automatic mode may not always be preferred - read the
options page for further details on the difference between automatic and manual.

## Why am I getting checks earlier than when I should be?

Most effect locations, some events and NPCs are only possible once per save.
Because of this, the code that checks for locations will usually be overly
lenient, in many cases only requiring you to be in the right place, rather than
interacting with the needed object. This prevents softlocks if the client isn't
loaded when the one-time event happens and makes manual mode possible without
save trickery.

## How do I get a check if the associated NPC is gone in this save?

See above - simply visit the correct area, and you should be able to send the
check. You may need to cross-reference the location map to see where the NPC
should typically be, and visit the specific tile.

## Which versions of the game does this work with?

This APWorld is compatible with version **0.129 patch 16**.

## The version on YNO is more recent than the version listed above, what do I do?

Newer versions should still mostly work to completion. As the data gathering
process is mostly automated, new APWorld versions should come out relatively
quickly after a Yume 2kki update gets pushed out to YNO.

Currently, there is no special procedure for handling YNO updates mid-session.
In the future, tools may be offered to downgrade the YNO version to a
locally-hosted version of Yume 2kki, but currently if the game ever updates in
a way that'd break logic or remove locations, you're going to have to ask your
game host to cheat them in.

## Where can I report issues?

In the Archipelago Discord server, navigate to
[#future-game-design > Yume 2kki \[YNO\]](https://discord.com/channels/731205301247803413/1483567293886763120)
to ask for help or report issues.
Alternatively, you may report issues on the [yno-ap GitHub repo.](https://github.com/oatmealine/yno-ap)
