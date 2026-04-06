import logging
import math

from BaseClasses import MultiWorld, Item, Tutorial, Location, Region, ItemClassification
from worlds.AutoWorld import World, CollectionState, WebWorld
from worlds.generic.Rules import add_rule
from typing import Dict, List, Callable

from .Options import Yume2kkiOptions, MinigameTreatment, KuraPuzzlesanity, Wallpapersanity, Goal, create_option_groups
from .data import items as item_data, locations as location_data, item_ids, location_ids, world_data, Yume2kkiItemData, Yume2kkiLocationData, Yume2kkiItemType, Yume2kkiLocationType, ConnType

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


class Yume2kkiWorld(World):
    game = "Yume 2kki"
    web = Yume2kkiWeb()
    item_name_to_id = {data.name: id for id, data in item_ids.items()}
    location_name_to_id = {data.name: id for id, data in location_ids.items()}
    options_dataclass = Yume2kkiOptions
    options: Yume2kkiOptions

    origin_region_name = "Urotsuki's Room"

    items: List[str] = []
    locations: List[str] = []
    precollected_items: List[str] = []

    def generate_early(self):
        possible_starters = self.options.starting_nexus_keys
        nexus_keys = [
            item.name for item in item_data if item.name in possible_starters and possible_starters[item.name]
        ]

        self.precollected_items.append("Bike")
        self.precollected_items.append(self.random.choice(nexus_keys))

        logger.debug(f"Yume 2kki: {self.player_name}: precollected_items = {self.precollected_items}")

        for item in item_data:
            if item.type == Yume2kkiItemType.MINIGAME and self.options.minigame_treatment != MinigameTreatment.option_locations:
                continue
            if item.type == Yume2kkiItemType.FILLER:
                continue

            self.items.append(item.name)

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
            if location.type == Yume2kkiLocationType.ENDING and not (location.name in self.options.ending_list and self.options.ending_list[location.name]):
                continue
            if location.name == "Ending #4" and self.options.wallpapersanity == Wallpapersanity.option_ignore:
                continue
            if location.name == "Bleak Future" and self.options.chance_threshold/100 < 1/64:
                continue

            self.locations.append(location.name)

        if self.options.locationsanity:
            locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.LOCATION]
            locations_amt = math.floor(self.options.locationsanity_percentage / 100 * len(locations))
            self.locations += self.random.sample(locations, locations_amt)

        if self.options.vmsanity:
            locations = [location.name for location in location_data if location.type == Yume2kkiLocationType.VENDING_MACHINE]
            locations_amt = math.floor(self.options.vmsanity_percentage / 100 * len(locations))
            self.locations += self.random.sample(locations, locations_amt)

    def create_items(self):
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
            item_pool.append(self.create_item("Filler")) # TODO

        self.multiworld.itempool += item_pool

    @staticmethod
    def item_type_to_classification(t: Yume2kkiItemType) -> ItemClassification:
        if t == Yume2kkiItemType.EFFECT:
            return ItemClassification.progression
        if t == Yume2kkiItemType.FILLER:
            return ItemClassification.filler
        if t == Yume2kkiItemType.MINIGAME:
            return ItemClassification.useful
        if t == Yume2kkiItemType.NEXUS_KEY:
            return ItemClassification.progression

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

        if self.options.goal == Goal.option_all_endings:
            victory_rule = lambda state: all(state.can_reach_location(ending, self.player) for ending in endings)
        elif self.options.goal == Goal.option_any_ending:
            victory_rule = lambda state: any(state.can_reach_location(ending, self.player) for ending in endings)

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

            if world["title"] + " - Partial" in regions:
                region.connect(regions[world["title"] + " - Partial"], f"{world["title"]} (Full -> Partial)")

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
                rules = []
                name = f"{world["title"]} -> {target_world["title"]}"

                t = connection["type"]

                # wiki marks all trophy room connections as dead-ends, but for our purposes they're fully accessible, just one-way
                if target_region.name == "Trophy Room":
                    t = 0

                if t & ConnType.NO_ENTRY.value:
                    continue
                if t & ConnType.LOCKED.value:
                    rules.append(lambda state: state.can_reach_region(target_region.name, self.player))
                if t & ConnType.DEAD_END.value:
                    is_dead_end = True
                if t & ConnType.ISOLATED.value:
                    continue
                if t & ConnType.EFFECT.value:
                    effect_names = connection["typeParams"][str(ConnType.EFFECT.value)]["params"]
                    # fix inconsistencies
                    effect_names = effect_names.replace('Teru Teru Bozu', 'Teru Teru Bōzu')
                    effect_names = effect_names.replace('&comma;', ',')
                    effect_names = effect_names.replace('Gakuran', 'School Boy')
                    effects = [effect.strip() for effect in effect_names.split(',')]
                    for effect in effects:
                        item = next((item for item in item_data if item.name == effect), None)
                        if item is None:
                            logger.warning(f"Yume 2kki: unknown effect used for {name} connection: {effect}")
                    
                    rules.append(lambda state: state.has_all(effects, self.player))
                if t & ConnType.CHANCE.value:
                    chance = connection["typeParams"][str(ConnType.CHANCE.value)]["params"]
                    if chance == "0%":
                        logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - chance for connection unknown")
                        if self.options.chance_threshold == 100:
                            continue
                    elif float(chance[:-1]) < self.options.chance_threshold:
                        continue
                if t & ConnType.LOCKED_CONDITION.value:
                    # TODO
                    logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - stub; cond unimplemented ({connection["typeParams"][str(ConnType.LOCKED_CONDITION.value)]["params"]})")
                    continue
                if t & ConnType.EXIT_POINT.value:
                    continue
                if t & ConnType.SEASONAL.value:
                    if self.options.chance_threshold >= 25:
                        continue
                if t & ConnType.INACCESSIBLE.value:
                    continue
                if t & ConnType.TRACKED.value:
                    logger.warning(f"Yume 2kki: {world["title"]} -> {target_world["title"]} - tracked stub")
                    continue

                if region.name == "Nexus" and target_region.name != "Urotsuki's Room" and target_region.name in self.items:
                    rules.append(lambda state: state.has(target_region.name, self.player))

                if is_dead_end:
                    entrance = region.connect(regions[target_world["title"] + " - Partial"], name)
                else:
                    entrance = region.connect(target_region, name)

                for rule in rules:
                    add_rule(entrance, rule)

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
            region.locations.append(location)
            locations[location_name] = location
                

        # location specific logic

        for location in location_data:
            if location.logic is not None:
                logic = location.logic
                self.maybe_add_rule(locations, location.name, lambda state: logic(state, self))

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
            "TotalLocations": len(self.locations)
        }

        return slot_data

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)