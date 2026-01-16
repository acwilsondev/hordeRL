import random

from engine import core
from horderl.components.world_building.world_parameters import (
    get_forest_params,
    get_mountain_params,
    get_plains_params,
    get_swamp_params,
    get_tundra_params,
)
from horderl.i18n import t

from ...gui.easy_menu import EasyMenu


def set_world_params(scene):
    logger = core.get_logger(__name__)
    logger.info(f"setting worldbuilder params")

    options = scene.cm.get_one(
        "SystemControlOptions", entity=core.get_id("world")
    )

    if options.world_parameters_selecting or options.world_parameters_selected:
        logger.info(
            "world parameters already selected or in the process of selecting"
        )
        return

    options.world_parameters_selecting = True

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

        system_controller = scene.cm.get_one(
            "SystemControlOptions", entity=core.get_id("system_controller")
        )

        system_controller.world_parameters_selecting = False
        system_controller.world_parameters_selected = True

        logger.info(f"world parameters set: {params}")

    return out_fn