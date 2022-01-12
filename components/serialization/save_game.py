import logging
from dataclasses import dataclass

from components.actors.energy_actor import EnergyActor
from components.build_world_listeners.world_parameters import WorldParameters
from engine import palettes, core
from engine.serialization import serialization


@dataclass
class SaveGame(EnergyActor):
    energy_cost: int = EnergyActor.INSTANT

    def act(self, scene) -> None:
        # we don't want this object to get caught in the save game
        scene.cm.delete_component(self)

        self._log_info(f"attempting to save game")
        params = scene.cm.get_one(WorldParameters, entity=core.get_id("world"))
        serialization.save(scene.cm.get_serial_form(), f"./{params.get_file_name()}.world")
        self._log_info(f"save complete")
        scene.message("Game saved.", color=palettes.LIGHT_WATER)

