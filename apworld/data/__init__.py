import json
from importlib.resources import files
from typing import NamedTuple, Optional, List, Dict, Callable
import enum
from worlds.AutoWorld import World, CollectionState
from collections import defaultdict

world_data = []
wallpaper_data = []
vm_data = []

with files().joinpath("data.json").open() as file:
    data = json.load(file)
    world_data = data["worldData"]
    wallpaper_data = data["wallpaperData"]

with files().joinpath("vms.json").open() as file:
    data = json.load(file)
    vm_data = data

class Yume2kkiItemType(enum.Enum):
    EFFECT = "Effect"
    SPECIAL = "Special"
    NEXUS_KEY = "Nexus Key"
    MINIGAME = "Minigame"
    FILLER = "Filler" # TODO: figure out what filler should be

class Yume2kkiItemData(NamedTuple):
    name: str
    type: Yume2kkiItemType

# https://github.com/Flashfyre/Yume-2kki-Explorer/blob/master/src/conn-type.js
class ConnType(enum.Enum):
    ONE_WAY = 1
    """One-way - cannot return after taking this connection"""
    NO_ENTRY = 2
    """No Entry - can take this connection only from the other world's side"""
    UNLOCK = 4
    """Unlock - unlocks access to this area from the opposite entrance"""
    LOCKED = 8
    """Locked - locked until the other world has been accessed once"""
    DEAD_END = 16
    """Dead-End - takes you to a closed off area in the other world"""
    ISOLATED = 32
    """Isolated - part of a closed off area in the current world"""
    EFFECT = 64
    """Effect - requires an effect"""
    CHANCE = 128
    """Chance - requires a chance success"""
    LOCKED_CONDITION = 256
    """Locked Condition - conditionally locked"""
    SHORTCUT = 512
    """Shortcut - ???"""
    EXIT_POINT = 1024
    """Exit Point - ???"""
    SEASONAL = 2048
    """Seasonal - only accessible during a certain season (???)"""
    INACCESSIBLE = 4096
    """Inaccessible - take a guess"""
    TRACKED = 8192
    """Tracked - ???"""

items: List[Yume2kkiItemData] = []

items += [
    Yume2kkiItemData(name="Bike", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Boy", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Chainsaw", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Lantern", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Fairy", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Spacesuit", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Glasses", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Rainbow", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Wolf", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Eyeball Bomb", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Telephone", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Maiko", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Twintails", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Penguin", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Insect", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Spring", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Invisible", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="School Boy", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Plaster Cast", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Stretch", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Haniwa", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Trombone", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Cake", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Child", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Red Riding Hood", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Tissue", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Bat", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Polygon", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Teru Teru Bōzu", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Marginal", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Drum", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Grave", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Crossing", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Bunny Ears", type=Yume2kkiItemType.EFFECT),
    Yume2kkiItemData(name="Dice", type=Yume2kkiItemType.EFFECT),

    Yume2kkiItemData(name="Text Events", type=Yume2kkiItemType.SPECIAL),

    Yume2kkiItemData(name="Library", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Graveyard World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Geometry World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Marijuana Goddess World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Forest World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Garden World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Heart World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Toy World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Urotsuki's Dream Apartments", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Red Streetlight World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Trophy Room", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Mushroom World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Purple World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Cipher Keyboard", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Portrait Purgatory", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Pudding World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Rock World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Ornamental Plains", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Blue Eyes World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Deep Red Wilds", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Lamp Puddle World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Lemonade Edifice", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Night World", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Abstract Corrosions", type=Yume2kkiItemType.NEXUS_KEY),
    Yume2kkiItemData(name="Usugurai Residence", type=Yume2kkiItemType.NEXUS_KEY),

    Yume2kkiItemData(name="Minigame A", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="Red Blue Yellow", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="↑V↑", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="Kura Puzzle", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="Plated Snow Country", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="FUJI", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="Gimmick Runner", type=Yume2kkiItemType.MINIGAME),
    Yume2kkiItemData(name="Memory Game", type=Yume2kkiItemType.MINIGAME),

    Yume2kkiItemData(name="Filler", type=Yume2kkiItemType.FILLER),
]

class Yume2kkiLocationType(enum.Enum):
    LOCATION = "Location"
    VENDING_MACHINE = "Vending Machine"
    MASK = "Mask"
    EVENT = "Event"
    MINIGAME_GOAL = "Minigame Goal"
    KURA_PUZZLE = "Kura Puzzle"
    WALLPAPER = "Wallpaper"
    NPC = "NPC"
    ENDING = "Ending"
    EFFECT_UNLOCK = "Effect Unlock"

class Yume2kkiLocationData(NamedTuple):
    name: str
    type: Yume2kkiLocationType
    region: str
    logic: Optional[Callable[[CollectionState, World], bool]]
Yume2kkiLocationData.__new__.__defaults__ = (None,) * len(Yume2kkiLocationData._fields)

locations: List[Yume2kkiLocationData] = []


has_all_effects = lambda state, self: state.has_all(
    (item.name for item in items if item.type == Yume2kkiItemType.EFFECT), self.player
)
# TODO the wallpapersanity hardcoded enum here sucks
# i think ideally wallpapers should be switched to events
can_get_500_wallpapers = lambda state, self: self.options.wallpapersanity == 1 or len([
    location
    for location in locations
    if location.type == Yume2kkiLocationType.WALLPAPER and state.can_reach_location(location.name, self.player)
]) >= 500

locations += [
    # https://yume.wiki/2kki/Endings
    Yume2kkiLocationData(name="Ending #1", type=Yume2kkiLocationType.ENDING, region="Trophy Room", logic=has_all_effects),
    Yume2kkiLocationData(name="Ending #2", type=Yume2kkiLocationType.ENDING, region="Trophy Room", logic=has_all_effects),
    Yume2kkiLocationData(name="Ending #3", type=Yume2kkiLocationType.ENDING, region="Trophy Room", logic=has_all_effects),
    Yume2kkiLocationData(name="Ending #4", type=Yume2kkiLocationType.ENDING, region="Trophy Room",
        logic=lambda state, self: has_all_effects(state, self) and can_get_500_wallpapers(state, self)),
    Yume2kkiLocationData(name="Ending #-1", type=Yume2kkiLocationType.ENDING, region="Urotsuki's Room",
        logic=lambda state, self: has_all_effects(state, self)
            and state.can_reach_region("Flying Fish World", self.player)
            and state.can_reach_region("Rough Ash World", self.player)
            and state.can_reach_region("Green Neon World", self.player)),
    # logic for these is really difficult to implement
    #Yume2kkiLocationData(name="Ending #---", type=Yume2kkiLocationType.ENDING, region="Urotsuki's Room"),
    #Yume2kkiLocationData(name="Ending #...", type=Yume2kkiLocationType.ENDING, region="Urotsuki's Room"),
    Yume2kkiLocationData(name="Bleak Future", type=Yume2kkiLocationType.ENDING, region="Urotsuki's Dream Apartments"),
    Yume2kkiLocationData(name="Ending #?", type=Yume2kkiLocationType.ENDING, region="Urotsuki's Room",
        logic=lambda state, self: state.count_from_list((item.name for item in items if item.type == Yume2kkiItemType.EFFECT), self.player) >= 24),

    # https://yume.wiki/2kki/Effects
    Yume2kkiLocationData(name="Bike Item", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Urotsuki's Room",
        logic=lambda state, self: state.can_reach_region("Garden World", self.player) or state.can_reach_region("Portrait Purgatory", self.player)),
    Yume2kkiLocationData(name="Boy Outline", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Geometry World"),
    Yume2kkiLocationData(name="Chainsaw Item", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Hospital"),
    # found in 2 places
    Yume2kkiLocationData(name="Lantern Cave", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Forest World"),
    Yume2kkiLocationData(name="Large Lantern", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Rural Starflower Field"),
    Yume2kkiLocationData(name="Sprite", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Black Building"),
    Yume2kkiLocationData(name="Spacesuit Helmet", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Flying Fish World"),
    # found in 2 places
    Yume2kkiLocationData(name="Glasses Pedestal", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Dark Museum",
        logic=lambda state, self: state.has("Lantern", self.player)), # technically not required, but it's really annoying w/o it
    Yume2kkiLocationData(name="Glasses Splatter", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Night-Lost Atelier"),
    Yume2kkiLocationData(name="Rainbow", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Theatre World"),
    Yume2kkiLocationData(name="Ōkami", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Teleport Maze"),
    Yume2kkiLocationData(name="Medabomb", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Mini-Maze"),
    Yume2kkiLocationData(name="Pet Telephone", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Dark Room"),
    Yume2kkiLocationData(name="Maiko Ghost", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Shinto Shrine"),
    Yume2kkiLocationData(name="Pole Man", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Deciding Street",
        logic=lambda state, self: state.has("Telephone", self.player)),
    # this is the exact same location as the penguin game location, so i'm naming it differently even if it's wrong
    Yume2kkiLocationData(name="Penguin", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Penguin Game"),
    Yume2kkiLocationData(name="Bagefu", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Scenic Outlook"),
    Yume2kkiLocationData(name="Bane Jack", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Apartments"),
    Yume2kkiLocationData(name="Silhouette", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Invisible Maze"),
    Yume2kkiLocationData(name="Gakuran-kun", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Monochrome Feudal Japan"),
    Yume2kkiLocationData(name="Heishi-kun", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Japan Town"),
    Yume2kkiLocationData(name="Setsudan Kanja", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Blissful Clinic"),
    Yume2kkiLocationData(name="Dead Figure", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Graffiti Maze"),
    Yume2kkiLocationData(name="Tall Woman Silhouette", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Bodacious Rotation Station"),
    Yume2kkiLocationData(name="Gray Haniwa", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Haniwa Temple"),
    Yume2kkiLocationData(name="Flashing Trombonist", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Urotsuki's Room",
        logic=lambda state, self:
        (state.can_reach_region("Baddies Bar", self.player) and state.has_any(["Lantern", "Chainsaw", "Rainbow"], self.player)) or
        state.can_reach_region("Acoustic Lounge", self.player)
    ),
    Yume2kkiLocationData(name="Shimofuri-tan", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Cutlery World"),
    Yume2kkiLocationData(name="Plaid Egg", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Hourglass Desert"),
    Yume2kkiLocationData(name="Apple Tree", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Fairy Tale Woods"),
    Yume2kkiLocationData(name="Birch Apple Tree", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Birch Forest"),
    Yume2kkiLocationData(name="Tower Creature", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="White Fern World"),
    Yume2kkiLocationData(name="Houtai Ude", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Azure Arm Land"),
    Yume2kkiLocationData(name="Komorin", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Urotsuki's Room",
        logic=lambda state, self:
        (state.can_reach_region("Tribe Settlement", self.player) and state.has_all(["Teru Teru Bōzu", "Rainbow"], self.player) or state.has_any(["Fairy", "Spacesuit"], self.player)) or
        (state.can_reach_region("FC Basement", self.player) and state.has("Invisible", self.player))
    ),
    Yume2kkiLocationData(name="Polygon", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Urotsuki's Room",
        logic=lambda state, self: state.can_reach_region("Warehouse", self.player) or state.can_reach_region("The Desktop", self.player)),
    Yume2kkiLocationData(name="Paper Dolls", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Dark Alleys"),
    Yume2kkiLocationData(name="Marginal Vivid Worker", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Broken Faces Area"),
    Yume2kkiLocationData(name="Oil Drum", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Purple World"),
    Yume2kkiLocationData(name="Walking Grave", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Graveyard World"),
    Yume2kkiLocationData(name="Railroad Crossing Sign", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Heart World",
        logic=lambda state, self: state.count_from_list((item.name for item in items if item.type == Yume2kkiItemType.EFFECT), self.player) >= 15),
    Yume2kkiLocationData(name="Usamimi", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Eyeball Archives",
        logic=lambda state, self: state.can_reach_region("Library", self.player) and state.has("Glasses", self.player)),
    Yume2kkiLocationData(name="Saikoro-kun", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Acerola World"),

    # https://yume.wiki/Category:Yume_2kki_Characters
    Yume2kkiLocationData(name="???-tsuki", type=Yume2kkiLocationType.NPC, region="Urotsuki's Room",
        logic=lambda state, self:
        state.can_reach_region("Second Nexus", self.player) or
        state.can_reach_region("Gutter", self.player) or
        state.can_reach_region("Opal Ruins A", self.player)),
    # 01-kun too frequent for it to make sense
    Yume2kkiLocationData(name="Aojiru", type=Yume2kkiLocationType.NPC, region="Hospital"),
    # Bagefu accounted for under effects
    # Bane Jack accounted for under effects
    # Beniko too frequent for it to make sense
    Yume2kkiLocationData(name="Beret Sisters", type=Yume2kkiLocationType.NPC, region="Snowy Pipe Organ"),
    # Boutique-ko too frequent for it to make sense
    # Boy Outline accounted for under effects
    Yume2kkiLocationData(name="Ceru", type=Yume2kkiLocationType.NPC, region="Lost Forest"), # only really counting the one w/ the cutscene
    # Dead Figure accounted for under effects
    # Detective too frequent for it to make sense
    Yume2kkiLocationData(name="Elvis Masada", type=Yume2kkiLocationType.NPC, region="Elvis Masada's Place"),
    # Flashing Trombonist accounted for under effects
    # Gakuran-kun accounted for under effects
    # Gray Haniwa accounted for under effects
    Yume2kkiLocationData(name="Hakoko", type=Yume2kkiLocationType.NPC, region="Visine World"),
    # Haniwa-musume too frequent for it to make sense
    # Heishi-kun accounted for under effects
    # Houtai Ude accounted for under effects
    # Iona too frequent for it to make sense
    Yume2kkiLocationData(name="Jimbo", type=Yume2kkiLocationType.NPC, region="Urotsuki's Room",
        logic=lambda state, self: state.can_reach_region("Giant Desktop", self.player) or state.can_reach_region("Holiday Hell", self.player)),
    Yume2kkiLocationData(name="Kanban Otoko", type=Yume2kkiLocationType.NPC, region="Japan Town"),
    # Komorin accounted for under effects
    # Maiko Ghost accounted for under effects
    # Marginal Vivid Worker accounted for under effects
    Yume2kkiLocationData(name="Marina", type=Yume2kkiLocationType.NPC, region="Neon Sea"),
    # Medabomb accounted for under effects
    Yume2kkiLocationData(name="Megusuri Uri", type=Yume2kkiLocationType.NPC, region="Visine World"),
    # Monmon too frequent for it to make sense
    Yume2kkiLocationData(name="Mysterious Maid", type=Yume2kkiLocationType.NPC, region="Urotsuki's Room",
        logic=lambda state, self:
        # TODO this should respect Chance Threshold, but in a smart way;
        # eg. a chance threshold of 25% would only exclude this from being in logic if you only have 2 of the given locations available to you
        state.can_reach_region("Hospital", self.player) or
        state.can_reach_region("Train Tracks", self.player) or
        state.can_reach_region("Sky Kingdom", self.player) or
        state.can_reach_region("Construction Frame Building", self.player)
    ),
    # Ninchiundō too frequent for it to make sense
    Yume2kkiLocationData(name="Ninetails", type=Yume2kkiLocationType.NPC, region="Red Lily Lake"),
    Yume2kkiLocationData(name="Odoriko", type=Yume2kkiLocationType.NPC, region="Red Streetlight World"),
    Yume2kkiLocationData(name="Olive", type=Yume2kkiLocationType.NPC, region="Lost Forest"),
    Yume2kkiLocationData(name="Oni Musume", type=Yume2kkiLocationType.NPC, region="Dark Room"),
    # Ōkami accounted for under effects
    Yume2kkiLocationData(name="Painter-kun", type=Yume2kkiLocationType.NPC, region="Art Gallery"),
    # Pet Telephone accounted for under effects
    # Pole Man accounted for under effects
    # Puni way too frequent for it to make sense
    # Saikoro-kun accounted for under effects
    Yume2kkiLocationData(name="Seishonen", type=Yume2kkiLocationType.NPC, region="Urotsuki's Dream Apartments"),
    # Setsudan Kanja accounted for under effects
    # Shimako too frequent, really annoying to implement
    # Shimofuri-tan accounted for under effects
    # Silhouette accounted for under effects
    # Sniper-san too frequent for it to make sense
    # Sprite accounted for under effects
    # Surimuki too frequent for it to make sense
    # Sweets Musume accounted for under effects
    Yume2kkiLocationData(name="Twintail Monster", type=Yume2kkiLocationType.NPC, region="Broken Faces Area",
        logic=lambda state, self: state.has_any(["Glasses", "Twintails"], self.player)),
    # Usamimi accounted for under effects
    Yume2kkiLocationData(name="Victim", type=Yume2kkiLocationType.NPC, region="Snowy Forest"),
    # Walking Grave accounted for under effects
    Yume2kkiLocationData(name="Witch of Hatred", type=Yume2kkiLocationType.NPC, region="Urotsuki's Room",
        logic=lambda state, self: state.can_reach_region("Love Lodge", self.player) or state.can_reach_region("Cold Summer Flames", self.player)),
    Yume2kkiLocationData(name="Yume", type=Yume2kkiLocationType.NPC, region="Urotsuki's Room",
        logic=lambda state, self: state.can_reach_region("Dark Room", self.player) or state.can_reach_region("Tapir-San's Place", self.player)),

    # https://yume.wiki/2kki/Minor_Characters
    # this specific set of characters is for now grabbed directly from the 2kki manual npcs. bless you nullifi
    Yume2kkiLocationData(name="Ahogeko", type=Yume2kkiLocationType.NPC, region="False Shoal"),
    Yume2kkiLocationData(name="Spider Queen", type=Yume2kkiLocationType.NPC, region="Spiders' Nest"),
    Yume2kkiLocationData(name="Firehead", type=Yume2kkiLocationType.NPC, region="Aquatic Cube City"),
    Yume2kkiLocationData(name="Operator Cyborg", type=Yume2kkiLocationType.NPC, region="Rusty Urban Complex - Partial"),
    Yume2kkiLocationData(name="Hiboushi", type=Yume2kkiLocationType.NPC, region="Apartments"),
    Yume2kkiLocationData(name="Purple Haze", type=Yume2kkiLocationType.NPC, region="Vaporwave Mall"),
    Yume2kkiLocationData(name="Blue Haired DJ", type=Yume2kkiLocationType.NPC, region="Virtual City"), # orig. name Hatsune Miku
    # Map Girl no idea
    Yume2kkiLocationData(name="Zalgo", type=Yume2kkiLocationType.NPC, region="Magnet Room"),
    Yume2kkiLocationData(name="The Lamplighter", type=Yume2kkiLocationType.NPC, region="Rainy Town"),
    Yume2kkiLocationData(name="Smile-san", type=Yume2kkiLocationType.NPC, region="Flying Fish World"),
    Yume2kkiLocationData(name="Alley Robot", type=Yume2kkiLocationType.NPC, region="Dark Alleys"),
    Yume2kkiLocationData(name="Shop Ruins Doctor", type=Yume2kkiLocationType.NPC, region="Shop Ruins"),
    Yume2kkiLocationData(name="Blob of Good Fortune", type=Yume2kkiLocationType.NPC, region="Sandstone Brick Maze"),
    Yume2kkiLocationData(name="Apartment Amoeba", type=Yume2kkiLocationType.NPC, region="Urotsuki's Dream Apartments"),
    Yume2kkiLocationData(name="Key Girl", type=Yume2kkiLocationType.NPC, region="Cotton Candy Haven"),
    Yume2kkiLocationData(name="Merlot", type=Yume2kkiLocationType.NPC, region="Cat Cemetery"),
    Yume2kkiLocationData(name="Midoriko", type=Yume2kkiLocationType.NPC, region="Checkerboard Clubhouse"),
    Yume2kkiLocationData(name="Waku Waku-san", type=Yume2kkiLocationType.NPC, region="Library"),

    # https://yume.wiki/2kki/Events
    Yume2kkiLocationData(name="Abuse", type=Yume2kkiLocationType.EVENT, region="Florist"),
    Yume2kkiLocationData(name="Amusement Park Clown Hell", type=Yume2kkiLocationType.EVENT, region="Underwater Amusement Park"),
    Yume2kkiLocationData(name="Ancient Rave", type=Yume2kkiLocationType.EVENT, region="Ancient Crypt"),
    Yume2kkiLocationData(name="Anetra's Rave", type=Yume2kkiLocationType.EVENT, region="Pinwheel Countryside"),
    Yume2kkiLocationData(name="Aooh", type=Yume2kkiLocationType.EVENT, region="Ahogeko's House"), # TODO: 1/64 chance
    Yume2kkiLocationData(name="Big Red", type=Yume2kkiLocationType.EVENT, region="Abandoned Factory"),
    Yume2kkiLocationData(name="Blood Sacrifice", type=Yume2kkiLocationType.EVENT, region="Blood World",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Book Return", type=Yume2kkiLocationType.EVENT, region="Eyeball Archives",
        logic=lambda state, self: state.can_reach_region("Library", self.player) and state.has("Glasses", self.player)),
    Yume2kkiLocationData(name="Buddha Rave", type=Yume2kkiLocationType.EVENT, region="Marijuana Goddess World"),
    Yume2kkiLocationData(name="Butcher's Wrath", type=Yume2kkiLocationType.EVENT, region="Mutant Pig Farm",
        logic=lambda state, self: state.has("Marginal", self.player)), # TODO: 1/1024 chance
    Yume2kkiLocationData(name="Chasers in Urotsuki's Room", type=Yume2kkiLocationType.EVENT, region="Urotsuki's Dream Apartments"), # TODO: 1/64 chance
    Yume2kkiLocationData(name="Chasers in the Woods", type=Yume2kkiLocationType.EVENT, region="Fairy Tale Woods"),
    Yume2kkiLocationData(name="The Cloning Room", type=Yume2kkiLocationType.EVENT, region="Red Brick Maze"),
    Yume2kkiLocationData(name="Giant Cloning Room", type=Yume2kkiLocationType.EVENT, region="Red Brick Maze",
        logic=lambda state, self: state.can_reach_location("Ending #4", self.player)), # TODO: 1/10 chance; exclude if ending #4 is excluded
    Yume2kkiLocationData(name="Clowns at the Circus", type=Yume2kkiLocationType.EVENT, region="Circus"),
    Yume2kkiLocationData(name="The Colossus of Rhomb", type=Yume2kkiLocationType.EVENT, region="Square-Square World",
        logic=lambda state, self:
            state.can_reach_location("Flying Fish World", self.player) or
            (state.can_reach_location("Cog Maze", self.player) and (state.can_reach_location("Japan Town", self.player) or True))), # TODO: replace True with unknown chance check
    Yume2kkiLocationData(name="Corrupted Nexus", type=Yume2kkiLocationType.EVENT, region="Nexus",
        # TODO: needs menu themes to be implemented
        # TODO: 1/1011 chance check
        #logic=lambda state, self: state.can_reach_location("Menu Theme #52", self.player)),
    ),
    Yume2kkiLocationData(name="Creatures of the Power Plant", type=Yume2kkiLocationType.EVENT, region="Power Plant"),
    Yume2kkiLocationData(name="The Cursed Corridor", type=Yume2kkiLocationType.EVENT, region="Execution Ground",
        logic=lambda state, self:
            state.can_reach_location("Atelier", self.player) and
            state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Decapitation", type=Yume2kkiLocationType.EVENT, region="Realistic Beach",
        logic=lambda state, self:
            (state.can_reach_location("Teleport Maze", self.player) or
            state.has_any(["Child", "Fairy", "Grave", "Dice"], self.player)) and
            state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="DECK RAVE", type=Yume2kkiLocationType.EVENT, region="Smiley Face DECK"),
    Yume2kkiLocationData(name="Dream of Roses", type=Yume2kkiLocationType.EVENT, region="Red Rock Caves",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Drowning", type=Yume2kkiLocationType.EVENT, region="Depths"),
    Yume2kkiLocationData(name="Duet with Elvis Masada", type=Yume2kkiLocationType.EVENT, region="Elvis Masada's Place",
        logic=lambda state, self: state.has("Trombone", self.player)),
    Yume2kkiLocationData(name="Duet with the Piano Girl", type=Yume2kkiLocationType.EVENT, region="Picture Book",
        logic=lambda state, self:
            state.can_reach_location("Rainy Docks", self.player) and
            state.has_any(["Fairy", "Spacesuit"], self.player) and
            state.has_any(["Spring", "Bat"], self.player) and
            state.has("Haniwa", self.player) and
            state.has_all(["Chainsaw", "Child"], self.player)), # TODO: 50% chance
    Yume2kkiLocationData(name="The Fisherman", type=Yume2kkiLocationType.EVENT, region="School",
        logic=lambda state, self: state.has("Penguin", self.player)),
    Yume2kkiLocationData(name="Flight", type=Yume2kkiLocationType.EVENT, region="Urotsuki's Dream Apartments"), # TODO: 1/9 chance
    Yume2kkiLocationData(name="The Flying Whale", type=Yume2kkiLocationType.EVENT, region="Paradise"), # TODO: 1/5 chance
    Yume2kkiLocationData(name="Flower Lady", type=Yume2kkiLocationType.EVENT, region="Apartments",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Fresh Bait", type=Yume2kkiLocationType.EVENT, region="Blizzard Plains"),
    Yume2kkiLocationData(name="Ghostly Ambush", type=Yume2kkiLocationType.EVENT, region="Rainy Town",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="The Graveyard's Sculpture", type=Yume2kkiLocationType.EVENT, region="Graveyard World",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Hallucination", type=Yume2kkiLocationType.EVENT, region="Laboratory",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Haniwa Dance", type=Yume2kkiLocationType.EVENT, region="Haniwa Temple",
        logic=lambda state, self: state.has("Haniwa", self.player)),
    Yume2kkiLocationData(name="The Haunted Cabinet", type=Yume2kkiLocationType.EVENT, region="Nostalgic House"),
    Yume2kkiLocationData(name="High Priestess", type=Yume2kkiLocationType.EVENT, region="Forest Carnival",
        logic=lambda state, self: state.has_all(["Chainsaw", "Crossing"], self.player)), # TODO: 1/5 chance
    Yume2kkiLocationData(name="Honoring the Dead", type=Yume2kkiLocationType.EVENT, region="Dream Mexico"),
    Yume2kkiLocationData(name="The Hospital Chainsaw Massacre", type=Yume2kkiLocationType.EVENT, region="Hospital"),
    Yume2kkiLocationData(name="Into the Mirror", type=Yume2kkiLocationType.EVENT, region="Jigsaw Puzzle World"),
    Yume2kkiLocationData(name="It Came From Behind", type=Yume2kkiLocationType.EVENT, region="Neon City"), # TODO: 1/2500 chance
    Yume2kkiLocationData(name="Japanese Turntables Event", type=Yume2kkiLocationType.EVENT, region="Urban Street Area",
        logic=lambda state, self: state.has("Fairy", self.player)),
    Yume2kkiLocationData(name="Lonely Urotsuki", type=Yume2kkiLocationType.EVENT, region="Underwater Amusement Park"),
    Yume2kkiLocationData(name="Madotsuki's Room", type=Yume2kkiLocationType.EVENT, region="Never-Ending Hallway"),
    Yume2kkiLocationData(name="Maiden Outlook Event", type=Yume2kkiLocationType.EVENT, region="Maiden Outlook"),
    Yume2kkiLocationData(name="March of Progress", type=Yume2kkiLocationType.EVENT, region="Chess World"),
    Yume2kkiLocationData(name="Mask Shop Ambush", type=Yume2kkiLocationType.EVENT, region="Mask Shop"),
    Yume2kkiLocationData(name="Masked Dance", type=Yume2kkiLocationType.EVENT, region="Opal Archives"),
    Yume2kkiLocationData(name="Mechanical Heart Act", type=Yume2kkiLocationType.EVENT, region="Amphitheater"),
    Yume2kkiLocationData(name="Mirror Urotsuki", type=Yume2kkiLocationType.EVENT, region="Day and Night Towers",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Monochrome Eye", type=Yume2kkiLocationType.EVENT, region="Flying Fish World"),
    Yume2kkiLocationData(name="Monochromatic Flying Creature", type=Yume2kkiLocationType.EVENT, region="Monochromatic Abyss"), # TODO: 1/2500 chance
    Yume2kkiLocationData(name="Mutation", type=Yume2kkiLocationType.EVENT, region="Parasite Laboratory",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="The Nail Lady", type=Yume2kkiLocationType.EVENT, region="Nail World",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Neon Sea Monster", type=Yume2kkiLocationType.EVENT, region="Neon Sea"), # TODO: 1/500 chance
    Yume2kkiLocationData(name="Nurie Event", type=Yume2kkiLocationType.EVENT, region="Library",
        logic=lambda state, self: state.can_reach_region("Bishop Cathedral", self.player) and state.has("Child", self.player)), # TODO: 1/48 chance
    Yume2kkiLocationData(name="Odorika's Dance", type=Yume2kkiLocationType.EVENT, region="Red Streetlight World",
        logic=lambda state, self: state.has("Maiko", self.player)),
    Yume2kkiLocationData(name="Operator Cyborg (event)", type=Yume2kkiLocationType.EVENT, region="Rusty Urban Complex - Partial",
        logic=lambda state, self: state.can_reach_region("Dream Pool", self.player) and state.has("Plaster Cast", self.player)),
    Yume2kkiLocationData(name="The Paying Customer", type=Yume2kkiLocationType.EVENT, region="Japan Town"),
    Yume2kkiLocationData(name="Peak Event", type=Yume2kkiLocationType.EVENT, region="Twisted Thickets",
        logic=lambda state, self: state.has("Lantern", self.player)),
    Yume2kkiLocationData(name="Photorealistic Event", type=Yume2kkiLocationType.EVENT, region="Fused Faces World"),
    Yume2kkiLocationData(name="Possessed by Yourself", type=Yume2kkiLocationType.EVENT, region="Static Noise Hell"),
    Yume2kkiLocationData(name="Resentment", type=Yume2kkiLocationType.EVENT, region="Crescent Tile World",
        logic=lambda state, self: state.has("Lantern", self.player)),
    Yume2kkiLocationData(name="Retaliation", type=Yume2kkiLocationType.EVENT, region="Gemstone Cave",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Rise and Shine!", type=Yume2kkiLocationType.EVENT, region="Pop Tiles Maze"),
    Yume2kkiLocationData(name="Rooftop", type=Yume2kkiLocationType.EVENT, region="Techno Condominium"),
    Yume2kkiLocationData(name="Seishonen's Glitched Room", type=Yume2kkiLocationType.EVENT, region="Urotsuki's Dream Apartments"), # TODO: 1/31 chance
    Yume2kkiLocationData(name="Screaming Forest", type=Yume2kkiLocationType.EVENT, region="Bright Forest"),
    Yume2kkiLocationData(name="Shadow Lady Forest", type=Yume2kkiLocationType.EVENT, region="Forest World",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Shadow Lady's Lap", type=Yume2kkiLocationType.EVENT, region="Toy World",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Sinister Smile", type=Yume2kkiLocationType.EVENT, region="Decrepit Village",
        logic=lambda state, self: state.has("Grave", self.player)),
    Yume2kkiLocationData(name="Spider Queen (event)", type=Yume2kkiLocationType.EVENT, region="Spiders' Nest",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Starry Night Event", type=Yume2kkiLocationType.EVENT, region="Planetarium"),
    Yume2kkiLocationData(name="Strange Image", type=Yume2kkiLocationType.EVENT, region="Flying Fish World",
        logic=lambda state, self: state.has("Telephone", self.player)),
    Yume2kkiLocationData(name="Surgical Ward's Facade", type=Yume2kkiLocationType.EVENT, region="Shop Ruins",
        logic=lambda state, self: state.has("Glasses", self.player)),
    Yume2kkiLocationData(name="The Spider's Web", type=Yume2kkiLocationType.EVENT, region="Fairy Tale Path",
        logic=lambda state, self: state.has_any(["Chainsaw", "Insect"], self.player) and state.can_reach_region("Bug Maze", self.player)),
    Yume2kkiLocationData(name="The Toxic Corruption", type=Yume2kkiLocationType.EVENT, region="Nerium Lab",
        logic=lambda state, self: state.can_reach_region("Pleasure Street", self.player) and state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Traffic Accident", type=Yume2kkiLocationType.EVENT, region="Splash Streetway"),
    Yume2kkiLocationData(name="Urotsuki's Execution", type=Yume2kkiLocationType.EVENT, region="Execution Ground",
        logic=lambda state, self: state.has("Chainsaw", self.player)),
    Yume2kkiLocationData(name="Vaporwave Event", type=Yume2kkiLocationType.EVENT, region="Virtual City"),
    Yume2kkiLocationData(name="Vertigo", type=Yume2kkiLocationType.EVENT, region="Urotsuki's Room",
        logic=lambda state, self: state.has("Chainsaw", self.player)), # TODO: unknown chance
    Yume2kkiLocationData(name="Vision", type=Yume2kkiLocationType.EVENT, region="Urotsuki's Room",
        logic=lambda state, self: state.has("Chainsaw", self.player)), # TODO: unknown chance
    Yume2kkiLocationData(name="Wardrobe Face", type=Yume2kkiLocationType.EVENT, region="Board Game Islands",
        logic=lambda state, self: state.has("Dice", self.player)), # TODO: unknown chance
    Yume2kkiLocationData(name="White Drooling Creature", type=Yume2kkiLocationType.EVENT, region="Apartments"),
    Yume2kkiLocationData(name="Woman and the Mirror", type=Yume2kkiLocationType.EVENT, region="Ocean Storehouse"), # TODO: 1/11 chance
    Yume2kkiLocationData(name="Watching and Warning Sign", type=Yume2kkiLocationType.EVENT, region="Foggy Remnants"),
    Yume2kkiLocationData(name="Zalgo (event)", type=Yume2kkiLocationType.EVENT, region="Magnet Room"),
    Yume2kkiLocationData(name="???-tsuki and the Liar's Vision", type=Yume2kkiLocationType.EVENT, region="Unknown Child's Room"), # TODO: 1/28 chance
    Yume2kkiLocationData(name="???-tsuki's Descent", type=Yume2kkiLocationType.EVENT, region="Second Nexus"),

    # https://yume.wiki/2kki/Masks
    # TODO
    # https://yume.wiki/2kki/Kura_Puzzles
    # TODO
    # https://yume.wiki/2kki/Menu_Themes
    # TODO
]

# location locations
locationsanity_blacklist = [
    "Urotsuki's Room",
    "Nexus",
    "Debug Room",
    "Game Console", # not even a world......
    "Developer Room",
]

for world in world_data:
    if world["title"] in locationsanity_blacklist:
        continue

    # logic handled by root apworld
    locations.append(Yume2kkiLocationData(
        name=world["title"],
        type=Yume2kkiLocationType.LOCATION,
        region=world["title"] + " - Partial"
    ))

# wallpaper locations
for wallpaper in wallpaper_data:
    # TODO logic
    locations.append(Yume2kkiLocationData(
        name=f"WP{wallpaper["wallpaperId"]} - {wallpaper["name"]}",
        type=Yume2kkiLocationType.WALLPAPER,
        region="Wallpapers"
    ))

# VM locations

vm_counts = defaultdict(int)

for vm in vm_data:
    location_name = vm["locationAlias"]
    vm_counts[location_name] += 1

# https://stackoverflow.com/a/47713392
ROMAN = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
    (   4, "IV"),
    (   1, "I"),
]

def to_roman(number):
    result = ""
    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result += roman * factor
    return result

vm_index = defaultdict(int)

for vm in vm_data:
    location_name = vm["locationAlias"]

    count = vm_counts[location_name]
    index = vm_index[location_name]

    name = f"Vending Machine - {location_name}"
    if count > 1:
        name += f" {to_roman(index + 1)}"
        vm_index[location_name] += 1

    locations.append(Yume2kkiLocationData(
        name=name,
        type=Yume2kkiLocationType.VENDING_MACHINE,
        region=vm["location"]
    ))

item_ids: Dict[int, Yume2kkiItemData] = {}
location_ids: Dict[int, Yume2kkiLocationData] = {}

id = 0
for item in items:
    id += 1
    item_ids[id] = item
id = 0
for location in locations:
    id += 1
    location_ids[id] = location