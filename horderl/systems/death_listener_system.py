"""System for handling death listener components when Die events fire."""

from __future__ import annotations

from engine import GameScene, constants, core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.logging import get_logger
from horderl.components.death_listeners.drop_gold import DropGold
from horderl.components.death_listeners.drop_log import DropFallenLog
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.death_listeners.on_die_emit_peasant_died import (
    OnDieEmitPeasantDied,
)
from horderl.components.death_listeners.player_corpse import PlayerCorpse
from horderl.components.death_listeners.schedule_rebuild import ScheduleRebuild
from horderl.components.death_listeners.terrain_changes_on_death import (
    TerrainChangedOnDeath,
)
from horderl.components.events.die_events import Die
from horderl.components.events.peasant_events import PeasantDied
from horderl.components.events.terrain_changed_event import TerrainChangedEvent
from horderl.components.events.tree_cut_event import TreeCutEvent
from horderl.components.house_structure import HouseStructure
from horderl.components.stomach import Stomach
from horderl.components.tree_cut_on_die import TreeCutOnDeath
from horderl.content import corpses, player_corpse
from horderl.content.getables.fallen_log import make_fallen_log
from horderl.content.getables.gold import make_gold_nugget


def _drop_gold(scene: GameScene, entity: int) -> None:
    for _listener in scene.cm.get_all(DropGold, entity=entity):
        get_logger(__name__).info(
            "dropped gold nugget on death",
            extra={"entity": entity},
        )
        coords = scene.cm.get_one(Coordinates, entity=entity)
        if not coords:
            continue
        scene.cm.add(*make_gold_nugget(coords.x, coords.y)[1])


def _drop_fallen_log(scene: GameScene, entity: int) -> None:
    for _listener in scene.cm.get_all(DropFallenLog, entity=entity):
        get_logger(__name__).info(
            "dropped fallen log on death",
            extra={"entity": entity},
        )
        coords = scene.cm.get_one(Coordinates, entity=entity)
        if not coords:
            continue
        scene.cm.add(*make_fallen_log(coords.x, coords.y)[1])


def _spawn_npc_corpse(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(Corpse, entity=entity):
        listener._log_info("spawned a corpse")
        entity_obj = scene.cm.get_one(Entity, entity=entity)
        coords = scene.cm.get_one(Coordinates, entity=entity)
        if not entity_obj or not coords:
            continue

        splatter = corpses.make_blood_splatter(
            5, coords.x, coords.y, listener.color, scene.config
        )
        if splatter:
            scene.cm.add(*splatter)
        scene.cm.add(
            *corpses.make_corpse(
                name=entity_obj.name,
                symbol=listener.symbol,
                x=coords.x,
                y=coords.y,
                color=listener.color,
            )[1]
        )


def _spawn_player_corpse(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(PlayerCorpse, entity=entity):
        listener._log_info("spawned a corpse")
        coords = scene.cm.get_one(Coordinates, entity=entity)
        if not coords:
            continue
        scene.cm.add(
            *corpses.make_blood_splatter(
                5, coords.x, coords.y, listener.color, scene.config
            )
        )
        scene.cm.add(
            *player_corpse.make_player_corpse(x=coords.x, y=coords.y)[1]
        )


def _schedule_rebuild(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(ScheduleRebuild, entity=entity):
        listener._log_info("scheduled rebuild")
        if listener.root == constants.INVALID:
            continue
        house_structure = scene.cm.get_one(
            HouseStructure, entity=listener.root
        )
        if house_structure:
            house_structure.is_destroyed = True


def _emit_terrain_changed(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(TerrainChangedOnDeath, entity=entity):
        listener._log_info("triggering, emitting TerrainChangedEvent")
        scene.cm.add(TerrainChangedEvent(entity=scene.player))


def _emit_peasant_died(scene: GameScene, entity: int) -> None:
    for _listener in scene.cm.get_all(OnDieEmitPeasantDied, entity=entity):
        scene.cm.add(PeasantDied(entity=core.get_id("world")))


def _dump_stomach(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(Stomach, entity=entity):
        listener._log_debug("on_die triggered, dumping contents")
        if listener.contents == constants.INVALID:
            listener._log_debug("nothing to dump")
            continue
        listener._log_debug(f"dumping {listener.contents}")
        scene.cm.unstash_entity(listener.contents)


def _emit_tree_cut(scene: GameScene, entity: int) -> None:
    for listener in scene.cm.get_all(TreeCutOnDeath, entity=entity):
        listener._log_debug("triggered")
        scene.cm.add(TreeCutEvent(entity=scene.player))


def _handle_die_event(scene: GameScene, event: Die) -> None:
    entity = event.entity
    _drop_gold(scene, entity)
    _drop_fallen_log(scene, entity)
    _spawn_npc_corpse(scene, entity)
    _spawn_player_corpse(scene, entity)
    _schedule_rebuild(scene, entity)
    _emit_terrain_changed(scene, entity)
    _emit_peasant_died(scene, entity)
    _dump_stomach(scene, entity)
    _emit_tree_cut(scene, entity)


def run(scene: GameScene) -> None:
    """
    Process Die events by applying death listener components on the affected entity.

    Args:
        scene: Scene providing the component manager and game state.

    Side Effects:
        - Spawns loot, corpses, or emits new events tied to death listeners.
        - Modifies state on related entities (e.g., house structures).
        - Unstashes entities contained in stomach components.
    """
    for event in list(scene.cm.get(Die)):
        _handle_die_event(scene, event)
