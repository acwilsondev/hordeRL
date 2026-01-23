"""System for handling season reset events.

Consumes components:
- AddFarmstead
- CollectTaxes
- CollectTaxesForKing
- CropsDieInWinter
- DieOnSeasonReset
- ExtractContractFees
- FreezeWater
- GrowGrass
- HealOnDally
- MovePeasantsOut
- Rebuilder
- ResetHealth
- SaveOnSeasonReset
- SpawnSaplingInSpring
- StationaryAttackActor
- UpgradeHouse
- WorldBeauty
"""

from __future__ import annotations

import random
from random import choice
from typing import List

from engine import GameScene
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl import palettes
from horderl.components import Appearance, Attributes
from horderl.components.abilities.build_wall_ability import BuildWallAbility
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.brains.stationary_attack_actor import (
    StationaryAttackActor,
)
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.events.delete_event import Delete
from horderl.components.events.die_events import Die
from horderl.components.house_structure import HouseStructure
from horderl.components.movement.heal_on_dally import HealOnDally
from horderl.components.relationships.farmed_by import FarmedBy
from horderl.components.relationships.resident import Resident
from horderl.components.season_reset_listeners.add_farmstead import (
    AddFarmstead,
)
from horderl.components.season_reset_listeners.collect_taxes import (
    CollectTaxes,
)
from horderl.components.season_reset_listeners.collect_taxes_for_king import (
    CollectTaxesForKing,
)
from horderl.components.season_reset_listeners.die_in_winter import (
    CropsDieInWinter,
)
from horderl.components.season_reset_listeners.die_on_season_reset import (
    DieOnSeasonReset,
)
from horderl.components.season_reset_listeners.extract_contract_fees import (
    ExtractContractFees,
)
from horderl.components.season_reset_listeners.grow_grass import GrowGrass
from horderl.components.season_reset_listeners.move_peasants_out import (
    MovePeasantsOut,
)
from horderl.components.season_reset_listeners.rebuilder import Rebuilder
from horderl.components.season_reset_listeners.reset_health import ResetHealth
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.season_reset_listeners.save_on_season import (
    SaveOnSeasonReset,
)
from horderl.components.season_reset_listeners.spawn_sapling_in_spring import (
    SpawnSaplingInSpring,
)
from horderl.components.season_reset_listeners.upgrade_houses import (
    UpgradeHouse,
)
from horderl.components.serialization.save_game import SaveGame
from horderl.components.tags.crop_info import CropInfo
from horderl.components.tags.peasant_tag import PeasantTag
from horderl.components.tags.tree_tag import TreeTag
from horderl.components.tax_value import TaxValue
from horderl.components.weather.freeze_water import FreezeWater
from horderl.components.weather.weather import Weather
from horderl.components.world_beauty import WorldBeauty
from horderl.content.farmsteads.houses import place_farmstead
from horderl.content.farmsteads.walls import make_wall
from horderl.content.terrain.roads import connect_point_to_road_network
from horderl.content.terrain.saplings import make_sapling
from horderl.i18n import t
from horderl.systems.brain_system import is_buildable
from horderl.systems.house_structure_system import get_house_structure_tiles


def run(scene: GameScene) -> None:
    """
    Execute season reset behavior for queued events.

    Args:
        scene: Active game scene with component manager access.

    Side Effects:
        - Spawns farms, saplings, and upgrades houses.
        - Adjusts taxes, health, and world state.
        - Deletes processed ResetSeason events.

    """
    for event in list(scene.cm.get(ResetSeason)):
        _announce_season(scene, event.season)
        _handle_season_reset(scene, event.season)
        scene.cm.delete_component(event)


def _announce_season(scene: GameScene, season: str) -> None:
    scene.message(
        t("message.season_begin", season=t(f"season.{season.lower()}"))
    )


def _handle_season_reset(scene: GameScene, season: str) -> None:
    for _listener in scene.cm.get(AddFarmstead):
        _add_farmstead(scene, season)
    for listener in scene.cm.get(CollectTaxes):
        _collect_taxes(scene, listener)
    for listener in scene.cm.get(CollectTaxesForKing):
        _collect_taxes_for_king(scene, listener, season)
    for _listener in scene.cm.get(CropsDieInWinter):
        _crops_die_in_winter(scene, season)
    for listener in scene.cm.get(DieOnSeasonReset):
        _die_on_season_reset(scene, listener)
    for listener in scene.cm.get(ExtractContractFees):
        _extract_contract_fees(scene, listener)
    for listener in scene.cm.get(FreezeWater):
        _resume_freezing(listener)
    for listener in scene.cm.get(GrowGrass):
        _grow_grass(scene, listener, season)
    for listener in scene.cm.get(HealOnDally):
        _reset_heal_counter(listener)
    for _listener in scene.cm.get(MovePeasantsOut):
        _move_peasants_out(scene, season)
    for listener in scene.cm.get(Rebuilder):
        _rebuild_house(scene, listener)
    for _listener in scene.cm.get(ResetHealth):
        _reset_health(scene)
    for listener in scene.cm.get(SaveOnSeasonReset):
        _autosave(scene, listener)
    for listener in scene.cm.get(SpawnSaplingInSpring):
        _spawn_saplings(scene, listener, season)
    for listener in scene.cm.get(StationaryAttackActor):
        _stationary_season_reset(scene, listener, season)
    for _listener in scene.cm.get(UpgradeHouse):
        _upgrade_houses(scene)
    for listener in scene.cm.get(WorldBeauty):
        _restore_world_beauty(listener, season)


def _add_farmstead(scene: GameScene, season: str) -> None:
    if season == "Spring":
        farmstead_id = place_farmstead(scene)
        farmstead_center = scene.cm.get_one(
            Coordinates, entity=farmstead_id
        ).position
        connect_point_to_road_network(scene, farmstead_center, trim_start=2)


def _collect_taxes(scene: GameScene, listener: CollectTaxes) -> None:
    listener._log_debug("collecting taxes from the village")
    taxes: List[TaxValue] = scene.cm.get(
        TaxValue, query=lambda tv: tv.value > 0
    )
    collected_taxes = sum(tax.value for tax in taxes)
    scene.message(
        t("message.collect_taxes", amount=collected_taxes),
        color=palettes.GOLD,
    )
    scene.gold += collected_taxes


def _collect_taxes_for_king(
    scene: GameScene, listener: CollectTaxesForKing, season: str
) -> None:
    if season != "Spring":
        scene.warn(t("warning.king_collects", amount=listener.value))
        return

    if scene.gold < listener.value:
        scene.popup_message(
            t(
                "popup.king_collects_insufficient",
                amount=listener.value,
                gold=scene.gold,
            )
        )
        scene.pop()
        return

    scene.gold -= listener.value
    old_value = listener.value
    listener.value += 25
    scene.popup_message(
        t(
            "popup.king_collects_paid",
            amount=old_value,
            next_amount=listener.value,
        )
    )


def _crops_die_in_winter(scene: GameScene, season: str) -> None:
    if season == "Winter":
        scene.message(
            "The peasants harvested the last of the crops before frost set in.",
            color=palettes.WATER,
        )
        crops = scene.cm.get(CropInfo, project=lambda ci: ci.entity)
        for crop in crops:
            scene.cm.delete(crop)


def _die_on_season_reset(scene: GameScene, listener: DieOnSeasonReset) -> None:
    scene.cm.add(Die(entity=listener.entity, killer=listener.entity))


def _extract_contract_fees(
    scene: GameScene, listener: ExtractContractFees
) -> None:
    listener._log_debug("extracting contract fees")
    taxes: List[TaxValue] = scene.cm.get(
        TaxValue, query=lambda tv: tv.value < 0
    )
    contract_fees = -1 * sum(tax.value for tax in taxes)

    if contract_fees == 0:
        return

    quitters = False
    while scene.gold < contract_fees:
        quitters = True
        random.shuffle(taxes)
        quitter = taxes.pop().entity
        scene.cm.add(Delete(entity=quitter))
        contract_fees = -1 * sum(tax.value for tax in taxes)

    if quitters:
        scene.warn(t("warning.contract_quitters"))
    if contract_fees > 0:
        scene.message(
            t("message.contract_fees", amount=contract_fees),
            color=palettes.GOLD,
        )
        scene.gold -= contract_fees


def _resume_freezing(listener: FreezeWater) -> None:
    listener._log_debug("unpausing freezing")
    listener.is_recharging = True


def _grow_grass(scene: GameScene, listener: GrowGrass, season: str) -> None:
    if season in {"Spring", "Summer"}:
        scene.cm.delete(listener.entity)


def _reset_heal_counter(listener: HealOnDally) -> None:
    listener.count = 0


def _move_peasants_out(scene: GameScene, season: str) -> None:
    peasants = scene.cm.get(PeasantTag)
    for peasant in peasants:
        farm_plots = scene.cm.get(
            FarmedBy,
            project=lambda x: x.entity,
            query=lambda x: x.farmer == peasant.entity,
        )
        target = choice(farm_plots)
        coords = scene.cm.get_one(Coordinates, entity=target)
        peasant_coords = scene.cm.get_one(Coordinates, entity=peasant.entity)

        peasant_coords.x = coords.x
        peasant_coords.y = coords.y

        actor = scene.cm.get_one(PeasantActor, entity=peasant.entity)

        if season != "Winter":
            actor.state = PeasantActor.State.FARMING
        else:
            actor.state = PeasantActor.State.WANDERING


def _rebuild_house(scene: GameScene, listener: Rebuilder) -> None:
    house_structure = scene.cm.get_one(HouseStructure, entity=listener.entity)
    if house_structure and house_structure.is_destroyed:
        if _get_living_residents(scene, listener.entity):
            _rebuild_house_structure(scene, house_structure)
        else:
            _delete_farms(scene, listener)
            scene.cm.delete(listener.entity)


def _get_living_residents(scene: GameScene, house_id: int) -> List[PeasantTag]:
    resident: Resident = scene.cm.get_one(Resident, entity=house_id)
    peasants: List[PeasantTag] = scene.cm.get(
        PeasantTag, query=lambda pt: pt.entity == resident.resident
    )
    return peasants


def _rebuild_house_structure(
    scene: GameScene, house_structure: HouseStructure
) -> None:
    coords = scene.cm.get_one(Coordinates, entity=house_structure.entity)
    x = coords.x
    y = coords.y
    upper_left = make_wall(house_structure.entity, x - 1, y - 1, piece="ul")
    upper_middle = make_wall(house_structure.entity, x, y - 1, piece="um")
    upper_right = make_wall(house_structure.entity, x + 1, y - 1, piece="ur")
    middle_left = make_wall(house_structure.entity, x - 1, y, piece="ml")
    middle_right = make_wall(house_structure.entity, x + 1, y, piece="mr")
    bottom_left = make_wall(house_structure.entity, x - 1, y + 1, piece="bl")
    bottom_middle = make_wall(house_structure.entity, x, y + 1, piece="bm")
    bottom_right = make_wall(house_structure.entity, x + 1, y + 1, piece="br")
    house_structure.upper_left = upper_left[0]
    house_structure.upper_middle = upper_middle[0]
    house_structure.upper_right = upper_right[0]
    house_structure.middle_left = middle_left[0]
    house_structure.middle_right = middle_right[0]
    house_structure.bottom_left = bottom_left[0]
    house_structure.bottom_middle = bottom_middle[0]
    house_structure.bottom_right = bottom_right[0]
    for wall in [
        upper_left,
        upper_middle,
        upper_right,
        middle_left,
        middle_right,
        bottom_left,
        bottom_middle,
        bottom_right,
    ]:
        scene.cm.add(*wall[1])

    house_structure.is_destroyed = False


def _delete_farms(scene: GameScene, listener: Rebuilder) -> None:
    listener._log_debug("deleting farms for house")
    resident_link: Resident = scene.cm.get_one(
        Resident, entity=listener.entity
    )
    if not resident_link:
        listener._log_warning(
            "House with no historical resident found, should not happen"
        )
        return

    resident_id = resident_link.resident

    farms: List[int] = scene.cm.get(
        FarmedBy,
        query=lambda fb: fb.farmer == resident_id,
        project=lambda fb: fb.entity,
    )

    for farm in farms:
        listener._log_debug(f"deleting farm #{farm}")
        scene.cm.delete(farm)


def _reset_health(scene: GameScene) -> None:
    scene.message(t("message.reset_health"))
    healths: List[Attributes] = scene.cm.get(Attributes)
    for health in healths:
        health.hp = health.max_hp


def _autosave(scene: GameScene, listener: SaveOnSeasonReset) -> None:
    if not scene.config.autosave_enabled:
        listener._log_info("autosave is disabled")
        return
    scene.cm.add(SaveGame(entity=scene.player))


def _spawn_saplings(
    scene: GameScene, listener: SpawnSaplingInSpring, season: str
) -> None:
    if season != "Spring":
        return

    listener._log_info("triggered")
    weather = scene.cm.get(Weather)
    if weather:
        weather = weather[0]
    else:
        listener._log_warning("no weather found")
        return

    tree_coords = [
        scene.cm.get_one(Coordinates, entity=tt.entity)
        for tt in scene.cm.get(TreeTag)
        if random.randint(0, 500) < weather.seasonal_norm
    ]

    count = 0
    for coords in tree_coords:
        count += 1
        x = coords.x
        y = coords.y
        plantable_tiles = [
            (x2, y2)
            for x2, y2 in get_3_by_3_box(x, y)
            if is_buildable(scene, x2, y2)
        ]
        target_tile = random.choice(plantable_tiles)
        scene.cm.add(*make_sapling(target_tile[0], target_tile[1])[1])
    listener._log_info(f"added {count} saplings")


def _stationary_season_reset(
    scene: GameScene, brain: StationaryAttackActor, season: str
) -> None:
    # Routes to brain system behavior to avoid duplicating logic.
    from horderl.systems.brain_system import on_stationary_season_reset

    on_stationary_season_reset(scene, brain, season)


def _upgrade_houses(scene: GameScene) -> None:
    masonry_ability = scene.cm.get_one(BuildWallAbility, entity=scene.player)
    max_upgrade = 2 if masonry_ability else 1

    house_structures = scene.cm.get(
        HouseStructure,
        query=lambda hs: hs.upgrade_level != max_upgrade
        and not hs.is_destroyed,
    )

    if not house_structures:
        return

    house_structure = choice(house_structures)
    upgrade = [palettes.WOOD, palettes.STONE][house_structure.upgrade_level]

    walls = get_house_structure_tiles(house_structure)
    for wall in walls:
        attributes = scene.cm.get_one(Attributes, entity=wall)
        attributes.hp = attributes.max_hp = attributes.max_hp + 20

        appearance = scene.cm.get_one(Appearance, entity=wall)
        appearance.color = upgrade

        corpse_def = scene.cm.get_one(Corpse, entity=wall)
        corpse_def.color = upgrade

    house_structure.upgrade_level += 1


def _restore_world_beauty(listener: WorldBeauty, season: str) -> None:
    if season == "Spring":
        listener._log_info("relationship with the spirits improved")
        listener.spirits_attitude += 1
        listener.spirits_wrath -= 1
        listener._log_info(
            f"improved wrath {listener.spirits_wrath} and attitude"
            f" {listener.spirits_attitude}"
        )
