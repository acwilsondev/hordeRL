from dataclasses import dataclass, field
from typing import Dict

from horderl import palettes
from horderl.components.actors.energy_actor import EnergyActor
from horderl.components.world_building.world_parameters import WorldParameters
from engine import core
from horderl.i18n import t


@dataclass
class SaveGame(EnergyActor):
    """
    Component that handles saving the game state to disk.

    SaveGame inherits from EnergyActor to integrate with the game's energy system,
    allowing save operations to be scheduled within the turn-based flow of the game.
    When activated, it serializes the entire component manager state and writes it
    to a file named after the current world parameters.

    The component removes itself from the component manager before saving to avoid
    recursive serialization of the save component itself. It also provides user
    feedback through the scene messaging system upon completion.

    Attributes:
        energy_cost (int): The energy cost of performing the save action.
                           Set to INSTANT by default to execute immediately.
        extra (Dict): Optional additional data to include in the save file,
                      provided as a dictionary that gets merged with the
                      serialized game state.

    """

    energy_cost: int = EnergyActor.INSTANT
    extra: Dict = field(default_factory=dict)

    def act(self, scene) -> None:
        """
        Execute the save game operation.

        This method is called by the energy system when this component's turn
        arrives in the action queue. It serializes the entire game state and
        saves it to disk using the world parameter's file name.

        The component first removes itself from the component manager to prevent
        it from being included in the saved state. Then it requests the serialized
        form of all components from the component manager and passes this data to
        the scene's save_game method along with any extra data provided.

        Args:
            scene: The active game scene containing the component manager and
                  serialization logic.

        Returns:
            None

        """
        # we don't want this object to get caught in the save game
        scene.cm.delete_component(self)

        self._log_info("attempting to save game")
        params = scene.cm.get_one(WorldParameters, entity=core.get_id("world"))
        scene.save_game(
            scene.cm.get_serial_form(),
            f"./{params.get_file_name()}.world",
            self.extra,
        )
        self._log_info("save complete")
        scene.message(t("message.game_saved"), color=palettes.LIGHT_WATER)
