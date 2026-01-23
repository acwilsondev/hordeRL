"""System for handling attack start events.

Consumes components:
- AbilityTracker
- FastForwardBrain
- FreezeWater
- GrowCrops
- HealOnDally
- MovePeasantsIn
- MovePlayerToTownCenter
- StationaryAttackActor
"""

from __future__ import annotations

from engine import GameScene, core
from engine.components import Coordinates
from horderl.components.ability_tracker import AbilityTracker
from horderl.components.actors.calendar_actor import Calendar
from horderl.components.attack_start_listeners.grow_crops import GrowCrops
from horderl.components.attack_start_listeners.move_peasants_in import (
    MovePeasantsIn,
)
from horderl.components.brains.fast_forward_actor import FastForwardBrain
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.brains.stationary_attack_actor import (
    StationaryAttackActor,
)
from horderl.components.events.attack_started_events import AttackStarted
from horderl.components.house_structure import HouseStructure
from horderl.components.movement.heal_on_dally import HealOnDally
from horderl.components.relationships.farmed_by import FarmedBy
from horderl.components.relationships.residence import Residence
from horderl.components.season_reset_listeners.move_player_to_town_center import (
    MovePlayerToTownCenter,
)
from horderl.components.tags.crop_info import CropInfo
from horderl.components.tags.tag import Tag, TagType
from horderl.components.tags.town_center_flag import TownCenterFlag
from horderl.components.weather.freeze_water import FreezeWater
from horderl.content.farmsteads.crops import make_crops


def run(scene: GameScene) -> None:
    """
    Execute attack start behavior for queued events.

    Args:
        scene: Active game scene with component manager access.

    Side Effects:
        - Updates components that react to attack start.
        - Spawns crops and moves peasants/player.
        - Deletes processed AttackStarted events.

    """
    for event in list(scene.cm.get(AttackStarted)):
        _handle_attack_start(scene)
        scene.cm.delete_component(event)


def _handle_attack_start(scene: GameScene) -> None:
    for tracker in scene.cm.get(AbilityTracker):
        _reset_ability_tracker(tracker)
    for brain in scene.cm.get(FastForwardBrain):
        _fast_forward_attack_start(scene, brain)
    for freezer in scene.cm.get(FreezeWater):
        _pause_freezing(freezer)
    for crops in scene.cm.get(GrowCrops):
        _grow_crops(scene, crops)
    for healer in scene.cm.get(HealOnDally):
        _reset_heal_counter(healer)
    for mover in scene.cm.get(MovePeasantsIn):
        _move_peasants_in(scene, mover)
    for mover in scene.cm.get(MovePlayerToTownCenter):
        _move_player_to_town_center(scene, mover)
    for brain in scene.cm.get(StationaryAttackActor):
        _stationary_attack_start(scene, brain)


def _reset_ability_tracker(tracker: AbilityTracker) -> None:
    tracker._log_debug("resetting ability to 0")
    tracker.current_ability = 0


def _fast_forward_attack_start(
    scene: GameScene, brain: FastForwardBrain
) -> None:
    # Routes to brain system behavior to avoid duplicating logic.
    from horderl.systems.brain_system import on_fast_forward_attack_start

    on_fast_forward_attack_start(scene, brain)


def _pause_freezing(freezer: FreezeWater) -> None:
    freezer._log_debug("pausing freezing")
    freezer.is_recharging = False


def _grow_crops(scene: GameScene, crops: GrowCrops) -> None:
    calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
    if not calendar or calendar.season > 2:
        return

    crop_info = scene.cm.get(
        CropInfo, query=lambda ci: ci.field_id == crops.entity
    )
    if crop_info:
        return

    crops._log_info("growing crops")
    farmed_by = scene.cm.get_one(FarmedBy, entity=crops.entity)
    farmer = farmed_by.farmer
    coords = scene.cm.get_one(Coordinates, entity=crops.entity)
    scene.cm.add(
        *make_crops(
            coords.x, coords.y, farmer, crops.entity, crops.crop_color
        )[1]
    )


def _reset_heal_counter(healer: HealOnDally) -> None:
    healer.count = 0


def _move_peasants_in(scene: GameScene, mover: MovePeasantsIn) -> None:
    mover._log_info("moving peasants into homes")
    peasants = scene.cm.get(
        Tag, query=lambda tag: tag.tag_type == TagType.PEASANT
    )
    for peasant in peasants:
        _move_peasant_home(scene, peasant)


def _move_peasant_home(scene: GameScene, peasant: Tag) -> None:
    home_address = scene.cm.get_one(Residence, entity=peasant.entity)
    possible_homes = scene.cm.get(HouseStructure)
    correct_home = next(
        (hs for hs in possible_homes if hs.house_id == home_address.house_id),
        None,
    )
    if correct_home:
        house_coords = scene.cm.get_one(
            Coordinates, entity=correct_home.entity
        )
        if house_coords:
            peasant_coords = scene.cm.get_one(
                Coordinates, entity=peasant.entity
            )
            if peasant_coords:
                peasant_coords.x = house_coords.x
                peasant_coords.y = house_coords.y
    peasant_actor = scene.cm.get_one(PeasantActor, entity=peasant.entity)
    peasant_actor.state = PeasantActor.State.HIDING


def _move_player_to_town_center(
    scene: GameScene, mover: MovePlayerToTownCenter
) -> None:
    mover._log_info("moving player to town center")
    flag = scene.cm.get(TownCenterFlag)[0]
    coord = scene.cm.get_one(Coordinates, entity=flag.entity)
    player = scene.cm.get_one(Coordinates, entity=scene.player)
    player.x = coord.x
    player.y = coord.y


def _stationary_attack_start(
    scene: GameScene, brain: StationaryAttackActor
) -> None:
    # Routes to brain system behavior to avoid duplicating logic.
    from horderl.systems.brain_system import on_stationary_attack_start

    on_stationary_attack_start(scene, brain)
