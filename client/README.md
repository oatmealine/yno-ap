## locations

### world visits

world visits are done just by sending every visited world as a location if
possible. don't see any drawbacks with this approach Just Yet

it tries to refer to wiki names whenever possible, but yno has a bunch of
overrides for scenarios such as subareas that the wiki doesn't keep track of and
there's not an easy mapping from one to the other, so the easiest suspects to
check through would be those overrides:
https://github.com/ynoproject/ynolocations/blob/master/2kki/config.json

### conditions

since we have the same data access as the server, and the server does all the
badge checking by itself, we can do badge checking. yno's badge system is pretty
powerful - you can see the docs here for a reference of what it can do:
https://github.com/ynoproject/ynobadges/blob/master/info/badge_tools.md

since checking for badges (specific events or milestones achieved by the player)
is pretty much equivalent to our location checks, we can reuse their
architecture, however the badge checking code needs to be reimplemented from the
grounds up since it is written in go, and not js. this is what checks.js does

the format in locations/ is very similar to yno's badge format, and most of the
data has been lifted from their badge definitions too to save a lot of work.
bless you yno crew for making all this stuff open source

#### yno-ap format documentation

##### `Location`

this is what each file in locations/ represents

- `name`: the name of the location. crosscheck w/ `apworld/data/__init__.py`
- `condition`: equivalent to `tag` in `badge`, except the condition is inlined.
if this is true, grant the location
- `conditions`: equivalent to `tags` in `badge`, except the condition is
inlined. if at least `conditionsCount` conditions are met, grant the location.
if `conditionsCount` is not set or 0, all conditions must be met

#### YNO format documentation

##### `Badge`

ref: https://github.com/ynoproject/ynoserver/blob/4eb93e74ea46088fec672b9812175b69a131f0a3/server/badges.go#L142

i've omitted things that don't affect conditions

- `reqType` (`string`): determines this badge's condition:
  - `tag`: if the condition named `reqString` is met, grant the badge
  - `tags`: if at least `reqCount` conditions from `reqStrings` are met, grant
  the badge. if `reqCount` is not set or 0, then all conditions must be met
  - `tagArrays`: if at least 1 condition from at least `reqCount` sets of
  conditions from `reqStringArrays` are met, grant the badge. you can think of
  this as `tags`, except that each condition can provide several alternative
  conditions to meet one of
  - `exp`, `expCount`, `expCompletion`: expedition related
  - `vmCount`: vm finder related
  - `badgeCount`
  - `locationCompletion`: sound room-esque visited location count check
  - `timeTrial`
  - `medal`
- `map`, `mapX`, `mapY`: despite seeming like these affect conditions, these
only exist to render the correct location in the YNO badge viewer. `mapX` and
`mapY` are here too because a single map can hold multiple locations

##### `Condition`

ref: https://github.com/ynoproject/ynoserver/blob/4eb93e74ea46088fec672b9812175b69a131f0a3/server/badges.go#L46

- `map` (`number`): the mapID this condition transpires in. although this is not
required, you should **almost always** specify it as this is the starting point
for all badge processing - the server will first figure out if the location the
client is in has any conditions, and _then_ start asking about each
switch/variable/event state. omitting it unneccessarily will lead to the client
constantly spamming packets

- `switchId` (`number`): switch ID to check for
- `switchValue` (`boolean`): which value `switchId` has to be
- `switchIds` (`number[]`): switch IDs to check for
- `switchValues` (`boolean[]`): which values `switchIds` have to be. only the
first switch is listened to for changes, and the rest are checked after it
passes the check
- `switchDelay` (`boolean`): only checks for conditions when the switch changes,
without doing an initial check when the room is entered

- `varId` (`number`): variable ID to check for
- `varValue` (`number`): which value `varId` has to be; see `varOp`
- `varValue2` (`number`): which value `varId` has to be; see `varOp`. only
applicable if `varOp` is `>=<`
- `varOp` (`string`): how to check for `varValue`:
  - `=` (default): `value = varValue`
  - `<`: `value < varValue`
  - `>`: `value > varValue`
  - `<=`: `value <= varValue`
  - `>=`: `value >= varValue`
  - `!=`: `value != varValue`
  - `>=<`: `varValue < value < varValue2`
- `varIds` (`number[]`): variable IDs to check for
- `varValues` (`number[]`): which values `varIds` have to be; see `varOps`. only
the first variable is listened to for changes, and the rest are checked after it
passes the check
- `varOps` (`string[]`): how to check for `varValues`. identical to `varOp`,
with the exception of `>=<`, as `varValues2` does not exist
- `varDelay` (`boolean`): only checks for conditions when the variable changes,
without doing an initial check when the room is entered
- `varTrigger` (`boolean`): sets what triggers the condition check if both
switch and variable checks are present; see the default `trigger` docs

- `trigger` (`string`): what triggers this condition. can be the following:
  - an empty string, for the default behavior. by default, all conditions
  are checked upon entering the map and whenever a relevant variable in the
  condition changes. when `varTrigger` is `false`, the switches specified by
  `switchId`/`switchIds` changing will set off the condition check, while when
  `varTrigger` is `true`, `varId`/`varIds` changing will set it off instead.
  - `event`, triggering when an event with an ID is triggered
  - `eventAction`, same as `event` except for "action events"(???)
  - `picture`, triggering when a picture with a certain name is shown
  - `coords`, triggering when the player's coordinates lie within `mapX1`,
  `mapX2`, `mapY1`, `mapY2`; see their documentation for details
  - `teleport`, like `coords` but only whenever a teleport occurs
  - `prevMap`, triggering on map entry and checking if `value` matches the
  previous map as reported by the client
- `value` (`string`): value used by `trigger` for the condition. see the
documentation there for what this value means for each type. **always a string**
- `values` (`string[]`): sets multiple possible valid values, and succeeds if
any one of them matches
- `mapX1` (`number`): used by the `coords`/`teleport` trigger types. if not left
undefined or set to `-1`, check if `x >= mapX1`
- `mapX2` (`number`): used by the `coords`/`teleport` trigger types. if not left
undefined or set to `-1`, check if `x <= mapX2`
- `mapY1` (`number`): used by the `coords`/`teleport` trigger types. if not left
undefined or set to `-1`, check if `y >= mapY1`
- `mapY2` (`number`): used by the `coords`/`teleport` trigger types. if not left
undefined or set to `-1`, check if `y <= mapY2`

- `timeTrial` (`boolean`): ???. not really worth looking into