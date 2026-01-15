from engine import core
from engine.game_scene import GameScene
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.content.player import make_player
from horderl.systems.build_world_system import set_world_params
from horderl.systems.build_world_system.mark_world_build_complete import (
    mark_world_build_complete,
)
from horderl.systems.build_world_system.place_flowers import place_flowers
from horderl.systems.build_world_system.place_lakes import place_lakes
from horderl.systems.build_world_system.place_peasants import place_peasants
from horderl.systems.build_world_system.place_river import place_river
from horderl.systems.build_world_system.place_roads import place_roads
from horderl.systems.build_world_system.place_rocks import place_rocks
from horderl.systems.build_world_system.place_trees import place_trees
from horderl.systems.build_world_system.set_world_params import (
    set_world_params,
)


def run(scene: GameScene) -> None:
    """Build the world according to the WorldParameters settings."""
    # TODO add a component gate for running this
    params = scene.cm.get_one(WorldParameters, entity=core.get_id("world"))
    if params and params.is_world_built:
        return
    
    logger = core.get_logger(__name__)
    logger.info(f"building world...")
    set_world_params(scene)
    _add_player(scene)
    place_lakes(scene)
    place_river(scene)
    place_peasants(scene)
    place_roads(scene)
    place_trees(scene)
    place_rocks(scene)
    place_flowers(scene)
    mark_world_build_complete(scene)
    logger.info(f"world build complete.")


def _add_player(scene: GameScene) -> None:
    # Add the player to the center of the map
    logger = core.get_logger(__name__)
    logger.info(f"adding player to map")
    player = make_player(
        scene.config.map_height // 2,
        scene.config.map_width // 2,
        scene.config,
    )
    scene.cm.add(*player[1])
