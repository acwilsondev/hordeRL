from engine import core
from engine.game_scene import GameScene
from horderl.components.worldbuilding_control import WorldbuildingControl
from horderl.content.player import make_player
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
    """Build the world according to the WorldParameters settings.

    Args:
        scene: Active game scene with worldbuilding components.

    Returns:
        None.

    Side effects:
        - Adds entities/components for terrain, NPCs, and player.
        - Removes the WorldbuildingControl component once complete.
        - Logs worldbuilding progress.
    """
    logger = core.get_logger(__name__)

    worldbuilding_control = scene.cm.get_one(
        WorldbuildingControl, entity=core.get_id("world")
    )
    if not worldbuilding_control:
        # we already built the world, nothing to do
        return

    # the first thing we need to do is prompt the user for biome selection
    if worldbuilding_control.world_parameters_selecting:
        # we can't move forward until the user has selected a biome
        return
    if worldbuilding_control.world_parameters_selected:
        # remove the worldbuilding control component, we are done with it
        logger.info("building world with selected parameters")
        _add_player(scene)
        place_lakes(scene)
        place_river(scene)
        place_peasants(scene)
        place_roads(scene)
        place_trees(scene)
        place_rocks(scene)
        place_flowers(scene)
        scene.cm.delete_component(worldbuilding_control)
        logger.info("world build complete")
        return

    # otherwise, we need to prompt the user to select a biome
    logger.info("prompting user to select world parameters")
    set_world_params(scene)


def _add_player(scene: GameScene) -> None:
    # Add the player to the center of the map.
    logger = core.get_logger(__name__)
    logger.info(f"adding player to map")
    player = make_player(
        scene.config.map_height // 2,
        scene.config.map_width // 2,
        scene.config,
    )
    scene.cm.add(*player[1])
