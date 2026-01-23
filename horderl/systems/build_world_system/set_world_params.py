import random

from engine import core
from horderl.components.worldbuilding_control import WorldbuildingControl
from horderl.i18n import t
from horderl.systems.world_building.params_factory import (
    get_forest_params,
    get_mountain_params,
    get_plains_params,
    get_swamp_params,
    get_tundra_params,
)

from ...gui.easy_menu import EasyMenu


def set_world_params(scene):
    """Prompt the player to select biome parameters for world generation.

    Args:
        scene: Active game scene used for component lookup and UI.

    Returns:
        None.

    Side effects:
        - Sets WorldbuildingControl selection state flags.
        - Adds an EasyMenu GUI element to the scene.
        - Logs selection prompts.
    """
    logger = core.get_logger(__name__)
    logger.info(f"setting worldbuilder params")

    control = scene.cm.get_one(
        WorldbuildingControl, entity=core.get_id("world")
    )
    if not control:
        logger.warning(
            "worldbuilding control missing; cannot set world parameters"
        )
        return

    control.world_parameters_selecting = True

    scene.add_gui_element(
        EasyMenu(
            t("menu.biome.title"),
            {
                t("menu.biome.plains_easy"): _get_settings(
                    scene, get_plains_params
                ),
                t("menu.biome.forest_moderate"): _get_settings(
                    scene, get_forest_params
                ),
                t("menu.biome.mountains_hard"): _get_settings(
                    scene, get_mountain_params
                ),
                t("menu.biome.swamp_hard"): _get_settings(
                    scene, get_swamp_params
                ),
                t("menu.biome.tundra_brutal"): _get_settings(
                    scene, get_tundra_params
                ),
            },
            scene.config.inventory_width,
            scene.config,
            on_escape=lambda: scene.pop(),
        )
    )


def _get_settings(scene, factory):
    def out_fn():
        params = factory(core.get_id("world"), scene.config)
        random.seed(params.world_seed)
        scene.cm.add(params)
        logger = core.get_logger(__name__)

        control = scene.cm.get_one(
            WorldbuildingControl, entity=core.get_id("world")
        )

        control.world_parameters_selecting = False
        control.world_parameters_selected = True

        logger.info(f"world parameters set: {params}")

    return out_fn
