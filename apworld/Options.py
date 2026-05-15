from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range, OptionDict, OptionGroup
from .data import items, locations, Yume2kkiItemType, Yume2kkiLocationType

class MinigameTreatment(Choice):
    """
    How to treat minigames:

    **Ignore:** Minigames have no bearing on the world; just a fun side distraction

    **Locations:** Completing certain tasks in minigames complete locations (eg. getting 2,500 score in FUJI), and the minigames themselves count as items

    **Hints:** Minigames are hint games that drop random hints when playing
    """
    display_name = "Minigame Treatment"
    option_ignore = 1
    option_locations = 2
    option_hints = 3
    default = 2

blacklisted_starters = [ "Trophy Room" ]

class StartingNexusKeys(OptionDict):
    """
    Determines which Nexus keys you can start with. A random one will be selected from this list on world generation.

    You will be able to get all Nexus keys as items, but this determines your initial restricted areas.
    """
    display_name = "Starting Nexus Keys"
    valid_keys = {key.name: True for key in items if key.type == Yume2kkiItemType.NEXUS_KEY}
    default = {key.name: key.name not in blacklisted_starters for key in items if key.type == Yume2kkiItemType.NEXUS_KEY}

class Goal(Choice):
    """
    Specifies the win condition:

    **Any Ending**: Get any ending from ending_list

    **All Endings**: Get all endings from ending_list
    """
    display_name = "Goal"
    option_any_ending = 1
    option_all_endings = 2
    default = 2

default_endings = [
    #"Bleak Future",
    "Ending #-1",
    "Ending #?",
    "Ending #1",
    "Ending #2",
    "Ending #3",
]

class EndingList(OptionDict):
    """
    Which endings to use for the **All Endings** win condition. Also specifies which endings should count as locations.

    Ending #4 will be ignored regardless of the setting here if Wallpapersanity is disabled, as then the world will have no clue how many wallpapers are logically accessible to the player.

    **Ending #--- and Ending #... are currently unimplemented.**
    """
    display_name = "Ending List"
    valid_keys = {ending.name: True for ending in locations if ending.type == Yume2kkiLocationType.ENDING}
    default = {ending.name: ending.name in default_endings for ending in locations if ending.type == Yume2kkiLocationType.ENDING}

class ChanceThreshold(Range):
    """
    The "reasonability" threshold for chance-based locations, as a percentage. In other words, your tolerance level of RPG Maker RNG bullshit.

    For instance, if set to 25, then any chance checks lower than 25% (1/4) will be excluded, and never required. Succeeding at them anyways will count as out-of-logic.

    This affects world connections and the Bleak Future ending.
    """
    display_name = "Chance Threshold"
    range_start = 0
    range_end = 100
    default = 1

# TODO
class HardNavigation(Toggle):
    """
    Determines when a region is counted as in logic.

    When disabled, a region will be counted as in logic if the shortest path is accessible. When enabled, a region will be counted as in logic if any path to it is available.
    
    This will significantly increase the tediousness of some checks, as there is no limit to how far an alternate path could go on for, and these paths are generally undocumented on the wiki.
    """
    display_name = "Hard Navigation"
    default = False

# TODO
class Masksanity(Toggle):
    """
    Buying masks from the Mask Shop will count as locations.
    """
    display_name = "Masksanity"
    default = True

# TODO
class Eventsanity(Toggle):
    """
    Triggering certain events will count as locations.
    The events that count for this are generally thee ones the Yume 2kki wiki considers as events: https://yume.wiki/2kki/Events
    """
    display_name = "Eventsanity"
    default = True

# TODO
class Wallpapersanity(Choice):
    """
    Whether to include getting wallpapers as locations.

    **Ignore:** Wallpapers do not do anything.

    **Unlocking:** Unlocking a wallpaper counts as a location.

    **Viewing:** Viewing the wallpaper on the PC counts as a location. Functionally the same as `unlocking`, but means the location sending is delayed until you wake up and check your PC again.
    """
    display_name = "Wallpapersanity"
    option_ignore = 1
    option_unlocking = 2
    option_viewing = 3
    default = 1

# TODO
class KuraPuzzlesanity(Choice):
    """
    Whether to include getting Kura Puzzles as locations.

    **Ignore:** Kura Puzzles do not do anything.

    **Unlocking:** Unlocking a Kura Puzzle counts as a location.

    **Solving:** Playing Kura Puzzle on the console and solving the puzzle after unlocking it counts as a location.
    """
    display_name = "Kura Puzzlesanity"
    option_ignore = 1
    option_unlocking = 2
    option_solving = 3
    default = 2

class NPCSanity(Toggle):
    """
    Interacting with certain NPCs will count as locations.
    The NPCs that count for this are generally the ones the Yume 2kki wiki considers as NPCs: https://yume.wiki/2kki/Minor_Characters#Non-Effect_NPCs

    Note that some NPCs will be included regardless of this toggle, as they are the NPCs that would usually give the player an effect.
    """
    display_name = "NPCSanity"
    default = True

class VMSanity(Toggle):
    """
    Every vending machine is a location.
    """
    display_name = "Vending Machinesanity"
    default = True

class VMSanityPercentage(Range):
    """
    How many vending machines to include as locations (as a percentage of all vending machines).
    """
    display_name = "Vending Machinesanity Percentage"
    range_start = 0
    range_end = 100
    default = 50

class VMSanityFilter(Toggle):
    """
    Only add vending machines in areas that are included by Locationsanity.

    If enabled without Locationsanity enabled, a set of locations will still be selected to filter vending machine areas by, but will not be added as locations.
    Increasing the VMSanity percentage and decreasing the Locationsanity percentage with this means vending machines will be less scattered about, instead coming in clumps.
    """
    display_name = "Vending Machinesanity Filter"
    default = True

class Locationsanity(Toggle):
    """
    Every in-game location is an Archipelago location.
    Ideally, keep only either VMSanity or this on, unless intentionally aiming for a really high location count.
    """
    display_name = "Locationsanity"
    default = False

class LocationsanityPercentage(Range):
    """
    How many locations to include as locations (as a percentage).
    I wouldn't ever recommend setting this to 100%. Do you really want to add ~1,500 locations?
    """
    display_name = "Location Percentage"
    range_start = 0
    range_end = 100
    default = 25

# TODO
class ExpeditionMode(Toggle):
    """
    Changes the Locationsanity location spread method to be more like YNO expeditions - a select few high depth locations are selected, and the stops to the shortest route to that location all also get included as locations. Results in a lot less scattered locations.
    """
    display_name = "Expedition Mode"
    default = True

@dataclass
class Yume2kkiOptions(PerGameCommonOptions):
    goal: Goal
    starting_nexus_keys: StartingNexusKeys
    minigame_treatment: MinigameTreatment
    ending_list: EndingList
    chance_threshold: ChanceThreshold
    hard_navigation: HardNavigation

    npcsanity: NPCSanity
    eventsanity: Eventsanity
    masksanity: Masksanity
    wallpapersanity: Wallpapersanity
    kura_puzzlesanity: KuraPuzzlesanity
    vmsanity: VMSanity
    vmsanity_percentage: VMSanityPercentage
    vmsanity_filter: VMSanityFilter
    locationsanity: Locationsanity
    locationsanity_percentage: LocationsanityPercentage
    expedition_mode: ExpeditionMode

option_groups: Dict[str, List[Any]] = {
    # this apparently overrides the default options. wild
    #"Game Options": [
    #    Goal,
    #    StartingNexusKeys,
    #    MinigameTreatment,
    #    EndingList,
    #    ChanceThreshold,
    #    HardNavigation,
    #],
    "Location Options": [
        NPCSanity,
        Eventsanity,
        Masksanity,
        Wallpapersanity,
        KuraPuzzlesanity,
        VMSanity, VMSanityPercentage, VMSanityFilter,
        Locationsanity, LocationsanityPercentage,
        ExpeditionMode,
    ]
}

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list