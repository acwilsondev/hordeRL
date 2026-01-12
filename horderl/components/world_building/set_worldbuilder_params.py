import random
from dataclasses import dataclass

from horderl.components.world_building.world_parameters import (
    get_forest_params,
    get_mountain_params,
    get_plains_params,
    get_swamp_params,
    get_tundra_params,
)
from horderl.engine import core
from horderl.engine.components.energy_actor import EnergyActor
from horderl.i18n import t

from ...content.world_builder import make_world_build
from ...gui.easy_menu import EasyMenu


def get_settings(scene, factory):
    def out_fn():
        params = factory(core.get_id("world"), scene.config)
        random.seed(params.world_seed)
        scene.cm.add(params, *make_world_build()[1])

    return out_fn


@dataclass
class SelectBiome(EnergyActor):
    def act(self, scene):
        self._log_info(f"setting worldbuilder params")
        scene.gui.add_element(
            EasyMenu(
                t("menu.biome.title"),
                {
                    t("menu.biome.plains_easy"): get_settings(
                        scene, get_plains_params
                    ),
                    t("menu.biome.forest_moderate"): get_settings(
                        scene, get_forest_params
                    ),
                    t("menu.biome.mountains_hard"): get_settings(
                        scene, get_mountain_params
                    ),
                    t("menu.biome.swamp_hard"): get_settings(
                        scene, get_swamp_params
                    ),
                    t("menu.biome.tundra_brutal"): get_settings(
                        scene, get_tundra_params
                    ),
                },
                scene.config.inventory_width,
                scene.config,
                on_escape=lambda: scene.pop(),
            )
        )
        scene.cm.delete_component(self)
