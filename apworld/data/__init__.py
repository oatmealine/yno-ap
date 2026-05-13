import json
from importlib.resources import files
from typing import NamedTuple, Optional, List, Dict, Callable
import enum
from worlds.AutoWorld import World, CollectionState

world_data = []
wallpaper_data = []

with files().joinpath("data.json").open() as file:
    data = json.load(file)
    world_data = data["worldData"]
    wallpaper_data = data["wallpaperData"]

class Yume2kkiItemType(enum.Enum):
    EFFECT = "Effect"
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
can_get_500_wallpapers = lambda state, self: len([
    state.can_reach_location(location.name, self.player)
    for location in locations if location.type == Yume2kkiLocationType.WALLPAPER
]) >= 500

locations += [
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
    Yume2kkiLocationData(name="Ookami", type=Yume2kkiLocationType.EFFECT_UNLOCK, region="Teleport Maze"),
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
]

# location locations
locationsanity_blacklist = [
    "Urotsuki's Room",
    "Nexus",
    "Debug Room",
    "Game Console", # not even a world......
]

for world in world_data:
    if world["title"] in locationsanity_blacklist:
        continue

    locations.append(Yume2kkiLocationData(
        name=world["title"],
        type=Yume2kkiLocationType.LOCATION,
        region=world["title"] + " - Partial"
    ))

# wallpaper locations
for wallpaper in wallpaper_data:
    locations.append(Yume2kkiLocationData(
        name=f"WP{wallpaper["wallpaperId"]} - {wallpaper["name"]}",
        type=Yume2kkiLocationType.WALLPAPER,
        region="Wallpapers"
    ))

item_ids: Dict[int, Yume2kkiItemData] = {}
location_ids: Dict[int, Yume2kkiLocationData] = {}

id = 29910000
for item in items:
    id += 1
    item_ids[id] = item
for location in locations:
    id += 1
    location_ids[id] = location