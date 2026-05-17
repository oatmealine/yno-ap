import logging
import math

from BaseClasses import MultiWorld, Item, Tutorial, Location, Region, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, CollectionState, WebWorld
from worlds.generic.Rules import add_rule
from typing import Dict, List, Callable

from .Options import Yume2kkiOptions, MinigameTreatment, KuraPuzzlesanity, Wallpapersanity, Goal, AuthorGating, create_option_groups
from .data import items as item_data, locations as location_data, item_ids, location_ids, world_data, Yume2kkiItemData, Yume2kkiLocationData, Yume2kkiItemType, Yume2kkiLocationType, ConnType, sanitize_author_name

logger = logging.getLogger("Yume 2kki")

class Yume2kkiWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yume 2kki for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["moonstruck.nectar"]
    )]

    option_groups = create_option_groups()

class Yume2kkiLocation(Location):
    game = "Yume2kki"

class Yume2kkiItem(Item):
    game = "Yume2kki"


forbidden_worlds = ["Debug Room"]

# entrances that are still useful in spite of being "redundant" depth-wise
hard_navigation_whitelist = [
    "Legacy Nexus -> Nexus",
    "Rooftops -> Symbolon"
]

# True if always accessible, False if always inaccessible, lambda otherwise
text_condition_logic = {
    # text events
    "Enable text events from the PC": 
        lambda state, self: state.has("Text Events", self.player),
    "Must have text events enabled": 
        lambda state, self: state.has("Text Events", self.player),
    "Disable text events from the PC": True,
    "Must have text events disabled": True,

    # spelling challenge success rate 100%
    "Spell \"UROTSUKI\" or enter Theatre World from the Eyeball Room in this area": True,
    "Spell \"SMILE\"": True,
    "Spell \"PAST\"": True,
    "Spell \"EYE\"": True,
    "Spell \"OCTAGON\"": True,
    "Spell \"UFO\"": True,
    "Spell \"WINDOW\"": True,
    "Spell \"PISCES\"": True,
    "Spell \"BATH\"": True,
    "Spell \"HOSPITAL\"": True,
    "Spell \"FREEZE\"": True,
    "Spell \"LIMBO\"": True,
    "Spell \"CAR\"": True,
    "Spell \"SQUARE\"": True,
    "Spell \"IKUSTORU\"": True,
    "Spell \"RED\"": True,

    # money
    "With 10夢": True,
    "With 10夢 or more in a low chance": True, # TODO undocumented chance
    "100夢": True,
    "Must pay 50夢 to the arcade machine": True,
    "200夢 each visit": True,
    "Must pay 500夢 to the Light Lady each time": True,

    # simple street
    "Enter the Hand Hub at least once":
        lambda state, self: state.can_reach_region("Hand Hub", self.player),
    "Enter Chocolate World at least once":
        lambda state, self: state.can_reach_region("Chocolate World", self.player),
    "Enter the Art Gallery at least once":
        lambda state, self: state.can_reach_region("Art Gallery", self.player),
    "Enter the Broken Faces Area at least once":
        lambda state, self: state.can_reach_region("Broken Faces Area", self.player),
    "Enter Theatre World at least once":
        lambda state, self: state.can_reach_region("Theatre World", self.player),
    "Enter the Gray Road at least once":
        lambda state, self: state.can_reach_region("Gray Road", self.player),
    "Enter the School at least once":
        lambda state, self: state.can_reach_region("School", self.player),
    "Enter the Intestines Maze at least once":
        lambda state, self: state.can_reach_region("Intestines Maze", self.player),
    "Enter Cipher Keyboard at least once":
        lambda state, self: state.can_reach_region("Cipher Keyboard", self.player),
    "Enter Parallel Graveyard at least once":
        lambda state, self: state.can_reach_region("Parallel Graveyard", self.player),
    "Enter the Cyber Hub at least once":
        lambda state, self: state.can_reach_region("Cyber Hub", self.player),

    # quarter flats
    # TODO: these are all accessible from Quarter Flats - Partial
    "Arrive from Blue Sanctuary":
        lambda state, self: state.can_reach_region("Blue Sanctuary", self.player),
    "Arrive from Somber Waterfront":
        lambda state, self: state.can_reach_region("Somber Waterfront", self.player),
    "Arrive from Pulsating Yellow Passage":
        lambda state, self: state.can_reach_region("Pulsating Yellow Passage", self.player),

    # bean worlds
    "Enter Legacy Nexus from each bedroom once":
        lambda state, self: all(state.can_reach_region(region, self.player) for region in [
            "Illuminated Building", "Blue Apartments", "Balloon Park"
        ]) and
        # balloon park requires night ver
        any(state.can_reach_region(region, self.player) for region in [
            "Worksite", "Bleeding Tree Disco", "Cerulean School"
        ]),
    "Enter the Nexus through the Realistic Flat in Legacy Nexus":
        lambda state, self: state.can_reach_entrance("Legacy Nexus -> Nexus", self.player),
    "Chainsaw if Underneath was entered from Flesh World":
        lambda state, self:
            state.has("Chainsaw", self.player) or
            any(state.can_reach_region(region, self.player) for region in [
                "ASCII Prairie", "Legacy of Ruin - Partial", "Monochrome Street"
            ]),
    "Chainsaw if Underneath was entered from Flesh World, and must have all 3 bedroom shortcuts unlocked in Legacy Nexus":
        lambda state, self:
            (state.has("Chainsaw", self.player) or
            any(state.can_reach_region(region, self.player) for region in [
                "ASCII Prairie", "Legacy of Ruin - Partial", "Monochrome Street"
            ])) and
            (lambda state, self: all(state.can_reach_region(region, self.player) for region in [
                "Illuminated Building", "Blue Apartments", "Balloon Park"
            ]) and
            # balloon park requires night ver
            any(state.can_reach_region(region, self.player) for region in [
                "Worksite", "Bleeding Tree Disco", "Cerulean School"
            ])),
    # TODO: should be accessible from Legacy of Ruin - Partial
    "Spring if the isolated section was entered from Underground Subway": lambda state, self: state.has("Spring", self.player),
    # balloon park
    "Night version only":
        lambda state, self: any(state.can_reach_region(region, self.player) for region in [
            "Worksite", "Bleeding Tree Disco", "Cerulean School"
        ]),
    "Day version only":
        lambda state, self: any(state.can_reach_region(region, self.player) for region in [
            "Underground Subway", "Dice Swamp"
        ]),

    # qxy worlds
    "Chainsaw the bleeding eye in the White Garden of Pure White Lands. This unlock is temporary & resets upon waking up":
        lambda state, self:
            # neccessary for seeing the eye
            state.has("Chainsaw", self.player) and all(state.can_reach_region(region, self.player) for region in [
                "Wooded Lakeside A", "Wooded Lakeside B", "Kaleidoscope World", "Critter Village", "Streetlight Docks"
            ]) and
            state.can_reach_region("Pure White Lands", self.player),
    "Must have arrived from the Shimako's Deluge event in Wooded Lakeside B. This unlock is temporary & resets upon waking up":
        lambda state, self:
            # TODO: the chances for this are weird... v#44 >= 128 and % 10 == 8?? the wiki is so vague about this
            state.can_reach_region("Wooded Lakeside B", self.player),
    "Sleep in the bed in the Sunset Hospital and then try to enter Home Within Nowhere":
        lambda state, self:
            # neccessary for Sunset Hospital access
            state.has("Chainsaw", self.player) and all(state.can_reach_region(region, self.player) for region in [
                "Wooded Lakeside A", "Wooded Lakeside B", "Kaleidoscope World", "Critter Village", "Streetlight Docks"
            ]),
    "Sleep in the bed in Sunset Hospital":
        lambda state, self:
            # neccessary for Sunset Hospital access
            state.has("Chainsaw", self.player) and all(state.can_reach_region(region, self.player) for region in [
                "Wooded Lakeside A", "Wooded Lakeside B", "Kaleidoscope World", "Critter Village", "Streetlight Docks"
            ]),
    "Access this area starting in Home Within Nowhere":
        lambda state, self:
            # the route is: Home Within Nowhere → Pure White Lands → Lamplit Stones → Adabana Gardens/Field of Cosmos → Bubble World → Red Sewers → Wooded Lakeside A → Oblique Hell → Wooded Lakeside B
            all(state.can_reach_region(region, self.player) for region in [
                "Home Within Nowhere", "Pure White Lands", "Lamplit Stones", "Bubble World", "Rew Sewers", "Wooded Lakeside A", "Oblique Hell"
            ]) and
            (state.can_reach_region("Adabana Gardens", self.player) or state.can_reach_region("Field of Cosmos", self.player)),
    "Enter all four transition hallways. The entrance will be in the last one": True,
    "Enter Red Sewers through Home Within Nowhere's route":
        lambda state, self:
            # the route is: Home Within Nowhere → Pure White Lands → Lamplit Stones → Adabana Gardens/Field of Cosmos → Bubble World → Red Sewers
            all(state.can_reach_region(region, self.player) for region in [
                "Home Within Nowhere", "Pure White Lands", "Lamplit Stones", "Bubble World"
            ]) and
            (state.can_reach_region("Adabana Gardens", self.player) or state.can_reach_region("Field of Cosmos", self.player)),
    "Enter the Red Sewers through Home Within Nowhere's route":
        lambda state, self:
            # the route is: Home Within Nowhere → Pure White Lands → Lamplit Stones → Adabana Gardens/Field of Cosmos → Bubble World → Red Sewers
            all(state.can_reach_region(region, self.player) for region in [
                "Home Within Nowhere", "Pure White Lands", "Lamplit Stones", "Bubble World"
            ]) and
            (state.can_reach_region("Adabana Gardens", self.player) or state.can_reach_region("Field of Cosmos", self.player)),
    "Enter the Red Sewers through Guts World":
        lambda state, self: state.can_reach_region("Guts World", self.player),
    "Enter Virtual City through Home Within Nowhere's route":
        lambda state, self:
            # the route is: Home Within Nowhere → Pure White Lands → Lamplit Stones → Adabana Gardens/Field of Cosmos → Bubble World → Red Sewers → Wooded Lakeside A → Oblique Hell → Glitched Butterfly Sector → Sierpinski Maze → Virtual City
            all(state.can_reach_region(region, self.player) for region in [
                "Home Within Nowhere", "Pure White Lands", "Lamplit Stones", "Bubble World", "Red Sewers", "Wooded Lakeside A", "Oblique Hell", "Glitched Butterfly Sector", "Sierpinski Maze"
            ]) and
            (state.can_reach_region("Adabana Gardens", self.player) or state.can_reach_region("Field of Cosmos", self.player)),

    # dream park
    "Having the path unlocked by entering from Graveyard World at least once":
        lambda state, self: state.can_reach_region("Graveyard World", self.player) and state.has_all(["Chainsaw", "Child", "Spring"], self.player),
    "Finding all of the Five Guardians":
        lambda state, self:
            # SHOULD be everything needed to solve the guardians' puzzles?
            state.has_all(["Fairy", "Chainsaw", "Child", "Penguin", "Stretch", "Lantern"], self.player) and state.can_reach_region("Apartments", self.player),
    "Viewing Ending #-1, breaking the egg in the Guardians' Temple and having the orbs show on each pillar":
        lambda state, self:
            state.can_reach_location("Ending #-1", self.player) and
            state.can_reach_region("Guardians' Temple", self.player),
    "Fulfilling the conditions to locating each entrance": True, # probably wrong but i cba
    "Awaken all three leading Lesser Guardians and unseal the Five Guardians":
        lambda state, self:
            state.can_reach_region("Guardians' Temple", self.player) and
            state.can_reach_region("Scrambled Egg Zone", self.player),

    # dreamland
    "Unlock at least one X mark": True,
    "If you visited this world before and entered from the south X in Dreamland":
        # TODO specify X world; undocumented in wiki
        lambda state, self: state.can_reach_region("Butter Rain World", self.player) and state.can_reach_region("Dreamland", self.player),
    "If you visited this world before and entered from the east X in Dreamland":
        # TODO specify X world; undocumented in wiki
        lambda state, self: state.can_reach_region("Cipher Fog World", self.player) and state.can_reach_region("Dreamland", self.player),
    "If you visited this world before and entered from the north X in Dreamland":
        # TODO specify X world; undocumented in wiki
        lambda state, self: state.can_reach_region("Sherbet Snowfield", self.player) and state.can_reach_region("Dreamland", self.player),
    "If you visited this world before and entered from the west X in Dreamland":
        # TODO specify X world; undocumented in wiki
        lambda state, self: state.can_reach_region("Sound Saws World", self.player) and state.can_reach_region("Dreamland", self.player),

    # visit unlockables
    "If the Second Nexus been visited before":
        lambda state, self: state.can_reach_region("Second Nexus", self.player),
    "Enter the Forest Pier at least once":
        lambda state, self: state.can_reach_region("Forest Pier", self.player),
    "Visit the Star Hub at least once":
        lambda state, self: state.can_reach_region("Star Hub", self.player),
    "Visit the Candlelit Factory at least once":
        lambda state, self: state.can_reach_region("Candlelit Factory", self.player),
    "Enter Container Forest at least once":
        lambda state, self: state.can_reach_region("Container Forest", self.player),
    "Visit Bikini Beach at least once":
        lambda state, self: state.can_reach_region("Bikini Beach", self.player),
    "Visit Theatre World at least once":
        lambda state, self: state.can_reach_region("Theatre World", self.player),
    "Visit the balcony in Guts World at least once":
        lambda state, self: state.can_reach_region("Guts World", self.player),
    "Visit Jigsaw Puzzle World at least once":
        lambda state, self: state.can_reach_region("Jigsaw Puzzle World", self.player),
    "Enter the Red Sewers at least once":
        lambda state, self: state.can_reach_region("Red Sewers", self.player),
    "Connection is isolated until the main area of Floating Tiled Islands has been visited at least once":
        lambda state, self: state.can_reach_region("Floating Tiled Islands", self.player),
    "Visit the Apartments at least once":
        lambda state, self: state.can_reach_region("Apartments", self.player),
    "Visit Kaprekar Number Zone at least once":
        lambda state, self: state.can_reach_region("Kaprekar Number Zone", self.player),
    "Enter the Silent Sewers at least once":
        lambda state, self: state.can_reach_region("Silent Sewers", self.player),
    "Visit the storefront in Somber Establishment once":
        lambda state, self: state.can_reach_region("Somber Establishment", self.player),
    "Visiting Stone World at least once":
        lambda state, self: state.can_reach_region("Stone World", self.player),
    "If the player has visited Icy Plateau before":
        lambda state, self: state.can_reach_region("Icy Plateau", self.player),
    "Enter Square-Square World at least once":
        lambda state, self: state.can_reach_region("Square-Square World", self.player),
    "Visit the Eyeball Room in Spelling Room  at least once":
        lambda state, self: state.can_reach_region("Spelling Room", self.player),
    "Enter Sugar Road at least once":
        lambda state, self: state.can_reach_region("Sugar Road", self.player),
    "Enter Megalith Grove at least once":
        lambda state, self: state.can_reach_region("Megalith Grove", self.player),
    "Enter the Mini-Nexus at least once":
        lambda state, self: state.can_reach_region("Mini-Nexus", self.player),
    "Isolated unless the door was unlocked in the following location":
        lambda state, self: state.can_reach_region("House of Vases", self.player),
    "Visiting Dream Venus at least once":
        lambda state, self: state.can_reach_region("Dream Venus", self.player),
    "Entering the Industrial Waterfront at least once":
        lambda state, self: state.can_reach_region("Tesla Garden", self.player),
    "If the player has visited Red Marbling World before":
        lambda state, self: state.can_reach_region("Red Marbling World", self.player),
    "Enter the Verdant Promenade at least once":
        lambda state, self: state.can_reach_region("Verdant Promenade", self.player),
    "Visit Candy World at least once":
        lambda state, self: state.can_reach_region("Candy World", self.player),
    "Connection makes Urotsuki stuck in a room unless Ehter Caverns was visited at least once":
        lambda state, self: state.can_reach_region("Ether Caverns", self.player),
    "Must have visited both Rainbow Silhouette World and Depths before":
        lambda state, self:
            state.can_reach_region("Rainbow Silhouette World", self.player) and
            state.can_reach_region("Depths", self.player),
    "If Abandoned Factory has been visited before":
        lambda state, self: state.can_reach_region("Abandoned Factory", self.player),
    "If Deserted Town has been visited before":
        lambda state, self: state.can_reach_region("Deserted Town", self.player),
    "If Bottom Garden has been visited before":
        lambda state, self: state.can_reach_region("Bottom Garden", self.player),
    "If the player has visited Cog Maze before":
        lambda state, self: state.can_reach_region("Cog Maze", self.player),
    "Visit Blue Sanctuary and the main area of Floating Tiled Islands once":
        lambda state, self:
            state.can_reach_region("Blue Sanctuary", self.player) and state.can_reach_region("Floating Tiled Islands", self.player),
    "Visit Wooden Block World":
        lambda state, self: state.can_reach_region("Wooden Block World", self.player),
    "Visit Flamelit Wasteland once":
        lambda state, self: state.can_reach_region("Flamelit Wasteland", self.player),
    "Reach the clover area in Candlelit Factory once":
        lambda state, self: state.can_reach_region("Candlelit Factory", self.player),
    "Visit Sepia Clouds World once":
        lambda state, self: state.can_reach_region("Sepia Clouds World", self.player),
    "Visit Elysium Pools once":
        lambda state, self: state.can_reach_region("Elysium Pools", self.player),
    "Visit Sepia Clouds World and enter the store in Somber Establishment once":
        lambda state, self:
            state.can_reach_region("Sepia Clouds World", self.player) and
            state.can_reach_region("Somber Establishment", self.player),
    "Visit Forest of Reflections at least once":
        lambda state, self: state.can_reach_region("Forest of Reflections", self.player),
    "Visit Indigo Pathway at least once":
        lambda state, self: state.can_reach_region("Indigo Pathway", self.player),
    "Visit Muffin Spice World at least once":
        lambda state, self: state.can_reach_region("Muffin Spice World", self.player),
    "Visit Twisted Forest at least once":
        lambda state, self: state.can_reach_region("Twisted Forest", self.player),
    "Visit Rainfall Forest at least once":
        lambda state, self: state.can_reach_region("Rainfall Forest", self.player),
    "If Fluorescent Halls has been visited before":
        lambda state, self: state.can_reach_region("Fluorescent Halls", self.player),
    "If the player has visited Fluorescent City before":
        lambda state, self: state.can_reach_region("Fluorescent Halls", self.player),
    "If the player has visited Fluorescent Halls before":
        lambda state, self: state.can_reach_region("Fluorescent Halls", self.player),
    "If the Second Nexus been visited before":
        lambda state, self: state.can_reach_region("Second Nexus", self.player),
    "Visit Ether Caverns at least once":
        lambda state, self: state.can_reach_region("Ether Caverns", self.player),
    "If the player has visited the Second Nexus before":
        lambda state, self: state.can_reach_region("Second Nexus", self.player),
    "If Grease Desert has been visited before":
        lambda state, self: state.can_reach_region("Grease Desert", self.player),
    "If you visited Head World before":
        lambda state, self: state.can_reach_region("Head World", self.player),
    "Visit Thunder Valley in the Elemental Caves":
        lambda state, self: state.can_reach_region("Elemental Caves", self.player),
    "Must have visited Firefly Clinic at least once":
        lambda state, self: state.can_reach_region("Firefly Clinic", self.player),
    "Must have visited Thundercloud Cells at least once":
        lambda state, self: state.can_reach_region("Thundercloud Cells", self.player),
    "Must have visited the Sculpture Exhibition at least once":
        lambda state, self: state.can_reach_region("Sculpture Exhibition", self.player),
    "Must have visited the Haunted Shipwreck Maze at least once":
        lambda state, self: state.can_reach_region("Haunted Shipwreck Maze", self.player),
    "Visit Collaged Complex B at least once":
        lambda state, self: state.can_reach_region("Collaged Complex B", self.player),
    "Visit Dreadful City at least once":
        lambda state, self: state.can_reach_region("Dreadful City", self.player),
    "Visit Red Desert Ruins at least once":
        lambda state, self: state.can_reach_region("Red Desert Ruins", self.player),

    # random specific ones
    "After seeing the first four endings":
        lambda state, self: all(state.can_reach_location(ending, self.player) for ending in ["Ending #1", "Ending #2", "Ending #3", "Ending #4"]),
    "Purchase an entry ticket at the museum": True,
    "Sleep at least 100 times": True, # god forgive me
    "When the UFO is present":
        lambda state, self:
            state.can_reach_region("Elvis Masada's Place", self.player) or # TODO: 25% chance
            state.can_reach_region("Spelling Room", self.player), # TODO: 1 in 6 chance
    "One-way if the UFO is present": True,
    "Obtain the Cake effect and enter Dream Park's central section at least once":
        lambda state, self: state.has("Cake", self.player) and state.can_reach_region("Dream Park", self.player),
    "Obtain the Teru Teru Bōzu effect and enter Dream Park's central section at least once":
        lambda state, self: state.has("Teru Teru Bōzu", self.player) and state.can_reach_region("Dream Park", self.player),
    "Enter the code OR access the Dark Room from the Tribe Settlement": True,
    "Visit the Dark Room from Hourglass Desert once":
        lambda state, self: state.can_reach_region("Hourglass Desert", self.player),
    "Obtained either the Bunny Ears effect or the Spring effect":
        lambda state, self: state.has_any(["Bunny Ears", "Spring"], self.player),
    "One-way until the player goes from Red Lily Lake to Candy World at least once": True,
    "Complete the area's puzzle once": True,
    "Visit Art Gallery at least once and have the Child effect in your inventory":
        lambda state, self: state.has("Child", self.player) and state.can_reach_region("Art Gallery", self.player),
    "Obtain Menu Theme #21 in Stone Towers":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #21", self.player),
        True,
    "Boutique-ko to be alive": True,
    "Obtain Menu Theme #38":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #38", self.player),
        True,
    "Can be accessed with the Spacesuit effect, in a 5% Chance or coming from Chocolate World":
        # TODO or 5% chance
        lambda state, self: state.can_reach_region("Chocolate World", self.player),
    "Must have Child effect":
        lambda state, self: state.has("Child", self.player),
    "Obtain the Boy effect and enter Dream Park's central section at least once":
        lambda state, self: state.has("Boy", self.player) and state.can_reach_region("Dream Park", self.player),
    "Obtain the Crossing effect and enter central Dream Park's central section at least once":
        lambda state, self: state.has("Crossing", self.player) and state.can_reach_region("Dream Park", self.player),
    "View Ending #1 at least once":
        lambda state, self: state.can_reach_location("Ending #1", self.player),
    "Go back and forth between the second and third stretch of the northeast road at least 20 times": True,
    "Sleep 90 times or more": True,
    "That the weather is snowy": True, # TODO gray road: unknown chance OR teru teru bozu
    "That the Commando or Provost-san mask is equipped":
        lambda state, self: state.can_reach_region("Docks", self.player),
    "Chainsaw if Polluted Swamp was entered from Underground Laboratory":
        lambda state, self:
            state.has("Chainsaw", self.player) or
            any(state.can_reach_region(region, self.player) for region in ["Symbolon", "Toxic Sea", "Rooftops"]),
    "Going through the cave or entering from the other side at least once":
        lambda state, self:
            state.can_reach_region("Teleport Maze", self.player) or
            state.has_any(["Child", "Fairy", "Grave", "Dice"], self.player),
    "Must chainsaw the fox NPC 7 times":
        lambda state, self: state.has("Chainsaw", self.player),
    "Go from Red Lily Lake to Candy World at least once":
        lambda state, self: state.has("Child", self.player),
    "Only if you entered from the Apartments":
        lambda state, self: state.can_reach_region("Apartments", self.player),
    "Have the Fairy effect":
        lambda state, self: state.has("Fairy", self.player),
    "Only accessible from the other side unless the player uses the Penguin and Fairy or Spacesuit effects":
        lambda state, self:
            state.can_reach_region("Urotsuki's Dream Apartments", self.player) or
            state.has("Penguin", self.player) and state.has_any(["Fairy", "Spacesuit"], self.player),
    "Enter Symbolon from the Rooftops":
        lambda state, self: state.can_reach_entrance("Rooftops -> Symbolon", self.player),
    "Complete the area's puzzle": True,
    "If number of times slept is divisible by 4": True,
    "If number of times slept divided by 4 has 1 as the remainder": True,
    "If number of times slept divided by 4 has 2 as the remainder": True,
    "If number of times slept divided by 4 has 3 as the remainder": True,
    "Accessible from this side with a mouse mask or the other side with certain masks":
        lambda state, self:
            # needed to unlock the mask
            state.has("Fairy", self.player) or
            state.can_reach_location("Bleak Future", self.player),
    "Leads to an isolated section with only the Magnet Room portal, unless the player has the Penguin and Fairy or Spacesuit effects":
        # TODO: technically inaccurate, Stone Maze - Partial should be accessible regardless and also link to Magnet Room
        lambda state, self: state.has("Penguin", self.player) and state.has_any(["Fairy", "Spacesuit"], self.player),
    "Enter the Mini-Nexus from Urotsuki's Dream Apartments at least once":
        lambda state, self: state.can_reach_entrance("Urotsuki's Dream Apartments -> Mini-Nexus", self.player),
    "Urotsuki had Slept 31 Times or Higher": True,
    "Certain masks to be equipped":
        # TODO unspecified on wiki, just assuming it's the same ones as the connection the opposite way
        lambda state, self: state.can_reach_entrance("Toy World -> Coffee Cup World", self.player),
    "Number of times that Urotsuki has dreamed must have an 8 as the last digit": True,
    "Only when the area has been entered for the last time from the opposite side. Not permanent":
        lambda state, self: state.can_reach_region("Smiley Signs World", self.player),
    "Only works once per save": True, # ??????? help me
    "At least 33 effects":
        lambda state, self: state.count_from_list((item.name for item in item_data if item.type == Yume2kkiItemType.EFFECT), self.player) >= 33,
    "Switch the lights off in the Liar's House in Lovesick World":
        lambda state, self: state.can_reach_region("Lovesick World", self.player),
    "Sleep in four specific beds":
        lambda state, self:
            state.can_reach_region("T-Folk World", self.player) and
            state.can_reach_region("Crazed Faces Maze", self.player) and
            state.can_reach_region("Blue Restaurant", self.player) and state.has_all(["Child", "Drum", "Crossing", "Chainsaw", "Trombone", "Rainbow", "Haniwa", "Boy", "Tissue", "Penguin", "School Boy", "Spring", "Eyeball Bomb", "Polygon", "Marginal"], self.player) and
            state.can_reach_region("Spiders' Nest", self.player),
    "Only if you came from this world": False,
    "Chainsaw if Orange Badlands was entered from Pudding World":
        lambda state, self:
            state.has("Chainsaw", self.player) or
            state.can_reach_region("Donut Hole World", self.player) or state.can_reach_region("Sunrise Road", self.player),
    "That the area is red":
        lambda state, self: state.has("Chainsaw", self.player),
    "The Wolf, Chainsaw, Eyeball Bomb and Marginal effects must not be equipped": True,
    "If Complex was accessed from Sai no Kawara":
        lambda state, self: state.can_reach_region("Sai no Kawara", self.player),
    "If Complex was accessed from Smooth Coastline":
        lambda state, self: state.can_reach_region("Smooth Coastline", self.player),
    "Visit the Twin Mountains Beach at least once": True,
    "Chainsaw the angel-looking statue":
        lambda state, self: state.has("Chainsaw", self.player),
    "View Ending #1":
        lambda state, self: state.can_reach_location("Ending #1", self.player),
    "Visit the Candlelit Factory":
        lambda state, self: state.can_reach_region("Candlelit Factory", self.player),
    "That you don't have the Drum effect":
        # my awesome trick #trick #awesome #trophyroom #favoriteeffect
        lambda state, self: state.can_reach_region("Trophy Room", self.player),
    "Press the buttons on the V, O, I, and D keys in order at least once": True,
    "If you did not enter from Smiling Trees World or Virtual City":
        lambda state, self:
            state.can_reach_region("Highway", self.player) or
            state.can_reach_region("River Road A", self.player) or
            state.can_reach_region("Christmas World", self.player),
    "This connection requires Chainsaw. This connection leads back to this area if Scribbled Worksite is entered through Crazy Pink House":
        lambda state, self: state.has("Chainsaw", self.player),
    "Chainsaw the Shadow Lady in the house and escape":
        lambda state, self: state.has("Chainsaw", self.player),
    "Amount of money must have 4 in every digit": True,
    "Visit this area at least once": True,
    "Inaccessible if the UFO is present": True, # TODO: 75% chance
    "View the cutscene in Bloodsoaked Pathways once and enable text events":
        lambda state, self:
            state.can_reach_region("Bloodsoaked Pathways", self.player) and
            state.has("Chainsaw", self.player) and
            state.has("Text Events", self.player),
    "Appears for a short time every 44 minutes": True, # sure why the hell not
    "Area must be gray and lifeless": True,
    "Must sit on the bench and throw 10夢 into the fountain": True,
    "Enter the area through Tribulation Complex":
        lambda state, self: state.can_reach_region("Tribulation Complex", self.player),
    "Enter the area through Redlight Alley":
        lambda state, self: state.can_reach_region("Redlight Alley", self.player),
    "Gather all 8 roses": True, # go my slenderman maze
    "Enter through Holiday Hell":
        lambda state, self: state.can_reach_region("Holiday Hell", self.player),
    "Enter through Redlight Alley":
        lambda state, self: state.can_reach_region("Redlight Alley", self.player),
    "Enter the area through Ice Cream Islands":
        lambda state, self: state.can_reach_region("Ice Cream Islands", self.player),
    "Enter the area through Redlight Alley":
        lambda state, self: state.can_reach_region("Redlight Alley", self.player),
    "Enter through Abandoned Grounds":
        lambda state, self: state.can_reach_region("Abandoned Grounds", self.player),
    "Enter through Redlight Alley":
        lambda state, self: state.can_reach_region("Redlight Alley", self.player),
    "Must interact with the bow in Thumbtack World once":
        lambda state, self: state.can_reach_region("Thumbtack World", self.player) and state.has("Child", self.player),
    "Enter through Test Facility":
        lambda state, self: state.can_reach_region("Test Facility", self.player),
    "Enter through Redlight Alley":
        lambda state, self: state.can_reach_region("Redlight Alley", self.player),
    "Enter the area through Platformer World":
        lambda state, self: state.can_reach_region("Platformer World", self.player),
    "Interacting with a tube with a green antenna in Copper Tube Desert":
        lambda state, self: state.has("Lantern", self.player) and state.can_reach_region("Copper Tube Desert", self.player),
    "Obtain Menu Theme 52":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #52", self.player),
        True,
    "After obtaining Menu Theme 52":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #52", self.player),
        True,
    "If Pink Life World was not entered from Miso Soup Dungeon":
        lambda state, self: state.can_reach_region("Warzone", self.player) or state.can_reach_region("Witch Heaven", self.player),
    "If Pink Life World was entered from Miso Soup Dungeon":
        lambda state, self: state.can_reach_region("Miso Soup Dungeon", self.player),
    "One-way unless Pink Life World was entered from Miso Soup Dungeon": True,
    "Cannot return to Pink Life World unless Pink Life World was entered from Miso Soup Dungeon": True,
    "Visit Red Desert Ruins: Passage, Dreadful City, or Collaged Complex B at least once":
        lambda state, self: any(state.can_reach_region(region, self.player) for region in [
            "Red Desert Ruins", "Dreadful City", "Collaged Complex B"
        ]),
    "Fairy, Spacesuit or Penguin effects if not in the sushi belt space":
        lambda state, self:
            state.has_any(["Fairy", "Spacesuit", "Penguin"], self.player) or
            state.can_reach_region("Humanism", self.player) or state.can_reach_region("Sushi Roll Swamp", self.player),
    "Interact With the Key-Girls": True,
    "Meet certain conditions": False, # TODO undocumented
    "Visit the Spiked Sands at least once and have the Plaster Cast effect":
        lambda state, self: state.can_reach_region("Spiked Sands", self.player) and state.has("Plaster Cast", self.player),
    "➡️ If entered from Garden World / ⛔ If entered from Bishop Cathedral":
        lambda state, self: state.can_reach_region("Garden World", self.player),
    "➡️ If entered from Bishop Cathedral / ⛔ If entered from Garden World":
        lambda state, self: state.can_reach_region("Bishop Cathedral", self.player),
    "➡️ If entered from Wrinked Fields and not entering from Entrails / ⛔ If entered from Entrails":
        lambda state, self: state.can_reach_region("Wrinkled Fields", self.player),
    "Complete the terminal puzzle": True,
    "Complete the Chase sequence event": True,
    "Accessed out of bounds":
        # It's possible to clip out of bounds using various effects
        # the wiki does not specify which, so TODO
        False,
    "Penguin effect if not coming from Dice Swamp B or this location":
        lambda state, self: state.can_reach_region("Dice Swamp", self.player) or state.has("Penguin", self.player),
    "Only requires Glasses if the chaser gallery has been completed at least once":
        lambda state, self: state.has("Glasses", self.player), # err on the side of caution and prevent softlocks
    "Complete the chaser gallery at least once": True,
    "Killing all four False Guardians":
        lambda state, self: state.has("Chainsaw", self.player) and all(state.can_reach_region(region, self.player) for region in [
            "Cipher Fog World", "Sound Saws World", "Butter Rain World", "Sherbet Snowfield"
        ]),
    "Enter the cone houses and interact with the NPCs in Abyssal Garden and Illusive Forest once":
        lambda state, self: state.can_reach_region("Abyssal Garden", self.player) and state.can_reach_region("Illusive Forest", self.player),
    "Interacting with the White Slime in Frozen Smile World with the Blue Slime mask, and using said mask on this location":
        lambda state, self: state.can_reach_region("Blue Eyes World", self.player) and state.can_reach_region("Frozen Smile World", self.player),
    "Visit the Neon Sewers at least once":
        lambda state, self: state.can_reach_region("Neon Sewers", self.player),
    "Leads to isolated section unless Chainsaw is acquired":
        lambda state, self: state.has("Chainsaw", self.player),
    "Isolated unless season is winter": True, # TODO 25% chance
    "Penguin after leaving the walls surrounding the door":
        lambda state, self: state.has("Penguin", self.player),
    "Visit the Police Chief's office in Dream Precinct at least once":
        lambda state, self: state.can_reach_region("Dream Precinct", self.player),
    "Chainsaw and Stretch if not coming from Fake Apartments":
        lambda state, self:
            state.can_reach_region("Fake Apartments", self.player) or
            state.has_all(["Chainsaw", "Stretch"], self.player),
    "Connection remains two-way as long as Urotsuki doesn't leave the rotted corridors":
        lambda state, self: state.can_reach_region("Underground Subway", self.player),
    "Connection remains two-way as long as Urotsuki doesn't leave the rotted corridors when entering from Fake Apartments":
        lambda state, self: state.can_reach_region("Underground Subway", self.player),
    "Accessible by going through the Rotted Corridors in Underground Subway":
        lambda state, self: state.can_reach_region("Underground Subway", self.player),
    "Only if coming from this location or entering here from any other connection": True,
    "Only if coming from this location": False,
    "Must enter Rifle Wasteland from Sniper-san's Room":
        lambda state, self: state.can_reach_region("Red Sun Outlook", self.player),
    "Isolated section from other side, unless door was unlocked": True,
    "Accessible by interacting with the NPC after meeting certain conditions":
        lambda state, self:
            state.can_reach_region("Colorless Rose Garden - Partial", self.player) and
            state.can_reach_region("Thumbtack World", self.player) and state.has("Child", self.player),
    "Connection leads to a blocked room until the player visits the main area of Somber Waterfront once":
        lambda state, self: state.can_reach_region("Somber Waterfront", self.player),
    "Accessible during the race": True,
    "Accessible if the day count/times slept counter on the PC ends in 5 before going to bed": True,
    "Connection is isolated unless Bat is set in the main area of Crow's Nest":
        lambda state, self: state.can_reach_region("Crow's Nest", self.player) and state.has("Bat", self.player),
    "Must have Child effect and have unlocked at least two of Spectral Hub's connections":
        lambda state, self:
            state.has("Child", self.player) and
            len([region for region in [
                "Dal Segno Labyrinth", "Ancient Stone Plates",
                "Fall Shoal", "Techno Rave Ruins",
            ] if state.can_reach_region(region, self.player)]) >= 2,
    "One-way unless Fluorescent City has been visited at least once": True,
    "Obtain Menu Theme #96":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #96", self.player),
        True,
    "Available if this area is entered through Crazy Pink House. One-way if entered from the opposite area":
        True,
    "Clear the hard mode in Obstacle Course 2":
        lambda state, self: state.can_reach_region("Obstacle Course 2", self.player) and state.has("Bike", self.player),
    "Must view Ending #3 at least once":
        lambda state, self: state.can_reach_location("Ending #3", self.player),
    "Have the Crossing effect":
        lambda state, self: state.has("Crossing", self.player),
    "Must have obtained Menu Theme #78 and pay 150夢 to the fisherman each time":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #78", self.player),
        True,
    "Interact with the mouth of the painting monster three times after getting all pieces of food":
        True,
    "Light up all four lanterns of the teleporter area": True,
    "If the world was entered from Goldfish Pond":
        lambda state, self: state.can_reach_region("Goldfish Pond", self.player),
    "If the world was entered from Turquoise Cityscape":
        lambda state, self: state.can_reach_region("Turquoise Cityscape", self.player),
    "Purchase an entry ticket in Museum of Curiosities":
        lambda state, self: state.can_reach_region("Museum of Curiosities", self.player),
    "Enter fish and knifes room and reach the end of the path": True,
    "Chainsaw rabbit girl and get money and not having Carnage Carnival shortcut":
        lambda state, self: state.has("Chainsaw", self.player), # TODO: 1/44 chance
    "See the steel tower in Moonlight Lantern Forest":
        lambda state, self: state.can_reach_region("Moonlight Lantern Forest", self.player),
    "Chainsaw the Tree of Life in Blood Cell Sea":
        lambda state, self: state.has("Chainsaw", self.player) and state.can_reach_region("Blood Cell Sea", self.player),
    "Enter from the Library":
        lambda state, self: state.can_reach_region("Library", self.player),
    "Isolated area requires Child effect. Full area requires visiting Innocent Dream once":
        lambda state, self: state.can_reach_region("Innocent Dream", self.player),
    "Must have visited any of the hospital rooms in Blissful Clinic":
        lambda state, self: state.can_reach_region("Blissful Clinic", self.player),
    "Must have visited the Building area in Quarter Flats":
        lambda state, self: state.can_reach_region("Quarter Flats", self.player),
    "Only one can be active from the rest": True, # technically possible even w/o dice
    "Obtain Menu Theme #57 and make sure text events are on":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #21", self.player) and state.has("Text Events", self.player),
        lambda state, self: state.has("Text Events", self.player),
    "Isolated if the season is spring": True, # TODO: 75% chance
    "After touching certain lamps in a specific manner, then using the rare variant of the Polygon effect once inside the alternative entrance":
        lambda state, self: state.has("Polygon", self.player), # TODO 1/32 chance
    "If the red switch in Hospital has been activated in the current dream session":
        lambda state, self: state.can_reach_region("Hospital", self.player),
    "1夢 or the Spring effect, and Menu Themes 6 and 7 must be unlocked":
        # TODO: menu themes have to be implemented first
        #lambda state, self: state.can_reach_location("Menu Theme #6", self.player) and state.can_reach_location("Menu Theme #7", self.player),
        True,
    "If this world was reached via Promnesic Terminal":
        lambda state, self: state.can_reach_entrance("Promnesic Terminal -> Solemn Meadow", self.player),
    "If this world was reached via Mystery Zone":
        lambda state, self: state.can_reach_entrance("Promnesic Terminal -> Mystery Zone", self.player),
}

class Yume2kkiWorld(World):
    game = "Yume 2kki"
    web = Yume2kkiWeb()
    item_name_to_id = {data.name: id for id, data in item_ids.items()}
    location_name_to_id = {data.name: id for id, data in location_ids.items()}
    options_dataclass = Yume2kkiOptions
    options: Yume2kkiOptions

    origin_region_name = "Urotsuki's Room"

    explicit_indirect_conditions = False

    items: List[str]
    locations: List[str]
    precollected_items: List[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []
        self.locations = []
        self.precollected_items = []

    #def generate_early(self):

    def create_items(self):
        possible_starters = self.options.starting_nexus_keys
        nexus_keys = [
            item.name for item in item_data if item.name in possible_starters and possible_starters[item.name]
        ]
        nexus_key = self.random.choice(nexus_keys)

        self.precollected_items.append("Bike")
        self.precollected_items.append(nexus_key)

        for item in item_data:
            if item.type == Yume2kkiItemType.MINIGAME and self.options.minigame_treatment != MinigameTreatment.option_locations:
                continue
            if item.type == Yume2kkiItemType.FILLER:
                continue
            if item.type == Yume2kkiItemType.AUTHOR and self.options.author_gating == AuthorGating.option_disable:
                continue

            self.items.append(item.name)
        
        if self.options.author_gating != AuthorGating.option_disable:
            for world_name in ["Urotsuki's Room", "Nexus", nexus_key]:
                world = next(w for w in world_data if w["title"] == world_name)
                for author in world["author"].split(", "):
                    author_name = sanitize_author_name(author)
                    if author_name not in self.precollected_items:
                        self.precollected_items.append(author_name)

        logger.debug(f"Yume 2kki: {self.player_name}: precollected_items = {self.precollected_items}")

        item_pool: List[Yume2kkiItem] = []

        for item_name in self.items:
            item = self.create_item(item_name)
            if item_name in self.precollected_items:
                self.multiworld.push_precollected(item)
            else:
                item_pool.append(item)

        # filler time
        total_location_count = len(self.multiworld.get_unfilled_locations(self.player))
        to_fill_location_count = total_location_count - len(item_pool)

        for i in range(to_fill_location_count):
            item_pool.append(self.create_filler())

        self.multiworld.itempool += item_pool
    
    def create_filler(self) -> Yume2kkiItem:
        return self.create_item("Filler") # TODO

    @staticmethod
    def item_type_to_classification(t: Yume2kkiItemType) -> ItemClassification:
        if t == Yume2kkiItemType.EFFECT:
            return ItemClassification(ItemClassification.progression + ItemClassification.useful)
        if t == Yume2kkiItemType.SPECIAL or t == Yume2kkiItemType.NEXUS_KEY or t == Yume2kkiItemType.AUTHOR:
            return ItemClassification.progression
        if t == Yume2kkiItemType.FILLER:
            return ItemClassification.filler
        if t == Yume2kkiItemType.MINIGAME:
            return ItemClassification.useful

    def create_item(self, name: str) -> Yume2kkiItem:
        data = next(i for i in item_data if i.name == name)

        return Yume2kkiItem(
            name,
            self.item_type_to_classification(data.type),
            self.item_name_to_id[name],
            self.player
        )

    # also: create_locations, since locations only matter with region associations
    def create_regions(self):
        for location in location_data:
            if location.type == Yume2kkiLocationType.EVENT and not self.options.eventsanity:
                continue
            if location.type == Yume2kkiLocationType.KURA_PUZZLE and self.options.kura_puzzlesanity == KuraPuzzlesanity.option_ignore:
                continue
            if location.type == Yume2kkiLocationType.LOCATION: # handled later
                continue
            if location.type == Yume2kkiLocationType.VENDING_MACHINE: # handled later
                continue
            if location.type == Yume2kkiLocationType.MASK and not self.options.masksanity:
                continue
            if location.type == Yume2kkiLocationType.NPC and not self.options.npcsanity:
                continue
            if location.type == Yume2kkiLocationType.MINIGAME_GOAL and self.options.minigame_treatment != MinigameTreatment.option_locations:
                continue
            if location.type == Yume2kkiLocationType.WALLPAPER and self.options.wallpapersanity == Wallpapersanity.option_ignore:
                continue

            self.locations.append(location.name)

        locationsanity_locations = []
        if self.options.locationsanity:
            locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.LOCATION]
            locations_amt = math.floor(self.options.locationsanity_percentage / 100 * len(locations))
            locationsanity_locations = self.random.sample(locations, locations_amt)
            self.locations += locationsanity_locations

        if self.options.vmsanity:
            locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.VENDING_MACHINE]
            if self.options.vmsanity_filter:
                locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.VENDING_MACHINE and location.region in locationsanity_locations]
            else:
                locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.VENDING_MACHINE]
            locations_amt = math.floor(self.options.vmsanity_percentage / 100 * len(locations))
            self.locations += self.random.sample(locations, locations_amt)

        regions: Dict[str, Region] = {}

        regions["Wallpapers"] = Region("Wallpapers", self.player, self.multiworld)
        regions["Kura Puzzles"] = Region("Kura Puzzles", self.player, self.multiworld)

        for world in world_data:
            if world["title"] in forbidden_worlds:
                continue

            region = Region(world["title"], self.player, self.multiworld)
            regions[region.name] = region
            region_partial = Region(world["title"] + " - Partial", self.player, self.multiworld)
            regions[region_partial.name] = region_partial
        
        # win condition

        victory_region = Region("Victory", self.player, self.multiworld)
        victory_location = Yume2kkiLocation(self.player, "Victory", None, victory_region)
        victory_region.locations.append(victory_location)
        victory_location.place_locked_item(
            Yume2kkiItem("Victory", ItemClassification.progression, None, self.player)
        )

        regions["Victory"] = victory_region

        endings = [location for location in self.locations if location in self.options.ending_list and self.options.ending_list[location]]

        victory_rule = lambda state: all(state.can_reach_location(ending, self.player) for ending in endings)

        regions["Urotsuki's Room"].connect(
            victory_region,
            rule=victory_rule
        )

        locations: Dict[str, Yume2kkiLocation] = {}

        # logic time!

        # basic region to region connections
        regions["Urotsuki's Room"].connect(regions["Wallpapers"], "Urotsuki's Room -> PC")
        regions["Urotsuki's Room"].connect(regions["Game Console"], "Urotsuki's Room -> Game Console")
        regions["Game Console"].connect(regions["Kura Puzzles"], "Game Console -> Kura Puzzles")

        # location connection & logic
        for world in world_data:
            if world["title"] not in regions:
                continue

            region = regions[world["title"]]
            connections = world["connections"]

            for connection in connections:
                target_id = connection["targetId"]
                target_world = next((world for world in world_data if world["id"] == target_id), None)
                if target_world is None:
                    logger.warning(f"Yume 2kki: Could not find world from ID {target_id}")
                    continue
                if target_world["title"] not in regions:
                    continue
                target_region = regions[target_world["title"]]

                is_dead_end = False
                is_exit_point = False
                rules = []
                name = f"{world["title"]} -> {target_world["title"]}"

                if not self.options.hard_navigation:
                    # using the wiki/explorer depths is unreliable
                    #if world["depth"] > target_world["depth"] and world["minDepth"] > target_world["minDepth"] and name not in hard_navigation_whitelist:
                    #    continue
                    # TODO come up with an alt solution
                    if False:
                        continue

                t = connection["type"]

                # wiki marks all trophy room connections as dead-ends, but for our purposes they're fully accessible, just one-way
                if target_region.name == "Trophy Room":
                    t = 0

                if t & ConnType.NO_ENTRY.value:
                    continue
                if t & ConnType.LOCKED.value:
                    rules.append(lambda state, target_region_name=target_region.name: state.can_reach_region(target_region_name, self.player))
                if t & ConnType.DEAD_END.value:
                    is_dead_end = True
                if t & ConnType.ISOLATED.value:
                    continue
                if t & ConnType.EFFECT.value:
                    effect_names = connection["typeParams"][str(ConnType.EFFECT.value)]["params"]
                    # fix inconsistencies
                    effect_names = effect_names.replace('Teru Teru Bozu', 'Teru Teru Bōzu')
                    effect_names = effect_names.replace('&comma;', ',')
                    effect_names = effect_names.replace(';', ',')
                    effect_names = effect_names.replace('Gakuran', 'School Boy')
                    effects = [effect.strip() for effect in effect_names.split(',')]
                    for effect in effects:
                        item = next((item for item in item_data if item.name == effect), None)
                        if item is None:
                            logger.warning(f"Yume 2kki: unknown effect used for {name} connection: {effect}")
                    
                    rules.append(lambda state, effects=effects: state.has_all(effects, self.player))
                if t & ConnType.CHANCE.value:
                    chance = connection["typeParams"][str(ConnType.CHANCE.value)]["params"]
                    if chance == "0%":
                        logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - chance for connection unknown")
                        if self.options.chance_threshold == 100:
                            continue
                    elif float(chance[:-1]) < self.options.chance_threshold:
                        continue
                if t & ConnType.LOCKED_CONDITION.value:
                    condition = connection["typeParams"][str(ConnType.LOCKED_CONDITION.value)]["params"]
                    if condition in text_condition_logic:
                        condition_logic = text_condition_logic[condition]
                        if condition_logic == False:
                            continue
                        elif condition_logic != True:
                            rules.append(lambda state, logic=condition_logic: logic(state, self))
                    else:
                        logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - stub; cond unimplemented ({condition})")
                        continue
                if t & ConnType.EXIT_POINT.value:
                    is_exit_point = True
                if t & ConnType.SEASONAL.value:
                    # TODO: fix for multiple possible seasons
                    if self.options.chance_threshold >= 25:
                        continue
                if t & ConnType.INACCESSIBLE.value:
                    continue
                if t & ConnType.TRACKED.value:
                    logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - tracked stub")
                    continue

                # nexus key check
                if region.name == "Nexus" and target_region.name != "Urotsuki's Room" and target_region.name in self.items:
                    rules.append(lambda state, item_name=target_region.name: state.has(item_name, self.player))

                # author gating check
                if self.options.author_gating != AuthorGating.option_disable:
                    authors = map(sanitize_author_name, target_world["author"].split(", "))
                    rules.append(lambda state, authors=authors: state.has_all(authors, self.player))

                # this is made with the foolish assumption that all dead ends in
                # a given location will connect, but not making this assumption
                # results in much more false negatives, leading to fill errors
                region_entrance = region
                region_exit = target_region
                if is_exit_point:
                    region_entrance = regions[world["title"] + " - Partial"]
                if is_dead_end:
                    region_exit = regions[target_world["title"] + " - Partial"]

                entrance = region_entrance.connect(region_exit, name)

                for rule in rules:
                    add_rule(entrance, rule)

            if world["title"] + " - Partial" in regions:
                region.connect(regions[world["title"] + " - Partial"], f"{world["title"]} (Full -> Partial)")

        # trim off inaccessible regions
        # does a flood fill type thing
        visited_regions = set()
        def walk(region):
            if region in visited_regions: return
            visited_regions.add(region)

            for exit_connection in region.exits:
                walk(exit_connection.connected_region)

        walk(regions["Urotsuki's Room"])

        remove_regions = [region.name for region in regions.values() if region not in visited_regions]

        logger.info(f"Yume 2kki: removed inaccessible regions: {remove_regions}")

        for region in remove_regions:
            del regions[region]

        # add region to location associations

        for location_name in self.locations:
            data = next(i for i in location_data if i.name == location_name)
            if not data.region in regions:
                logger.warning(f"Yume 2kki: {data.name} inaccessible because {data.region} is inaccessible; removing")
                continue

            region = regions[data.region]
            location = Yume2kkiLocation(self.player, data.name, self.location_name_to_id[data.name], region)

            if data.type == Yume2kkiLocationType.EFFECT_UNLOCK:
                location.progress_type = LocationProgressType.PRIORITY

            if data.type == Yume2kkiLocationType.ENDING and not (data.name in self.options.ending_list and self.options.ending_list[data.name]):
                location.progress_type = LocationProgressType.EXCLUDED
            if data.name == "Ending #4" and self.options.wallpapersanity == Wallpapersanity.option_ignore:
                location.progress_type = LocationProgressType.EXCLUDED
            if data.name == "Bleak Future" and self.options.chance_threshold/100 < 1/64:
                location.progress_type = LocationProgressType.EXCLUDED

            region.locations.append(location)
            locations[location_name] = location
                

        # location specific logic

        for location in location_data:
            if location.logic is not None:
                self.maybe_add_rule(locations, location.name, lambda state, logic=location.logic: logic(state, self))

        self.multiworld.regions += regions.values()

    def maybe_add_rule(self, locations: Dict[str, Yume2kkiLocation], name: str, rule: Callable[[object], bool], combine='and'):
        if name not in self.location_name_to_id:
            raise Exception(f"location {name} does not exist at all. is this a typo?")
        if name in locations:
            add_rule(locations[name], rule, combine=combine)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "Seed": self.multiworld.seed_name,
            "Slot": self.multiworld.player_name[self.player],
            "TotalLocations": len(self.locations),

            "client_mode": self.options.client_mode,

            "endings": 
                [location for location in self.locations if location in self.options.ending_list and self.options.ending_list[location]],
            "goal":
                self.options.goal,
        }

        return slot_data

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)