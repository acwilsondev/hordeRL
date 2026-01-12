from dataclasses import dataclass

from horderl.engine import core, palettes
from horderl.i18n import t
from horderl.engine.components.energy_actor import EnergyActor


@dataclass
class LoadGame(EnergyActor):
    """
    Component that handles loading a saved game state from disk.

    LoadGame inherits from EnergyActor to integrate with the game's energy system,
    allowing load operations to be scheduled within the turn-based flow of the game.
    When activated, it deserializes the game state from a specified file and
    reconstructs all game objects through the component manager.

    The component includes performance tracking to monitor load times, which is
    useful for optimization and debugging. It also provides user feedback through
    the scene messaging system upon completion.

    Attributes:
        energy_cost (int): The energy cost of performing the load action.
                           Set to INSTANT by default to execute immediately.
        file_name (str): Path to the save file that should be loaded.

    """

    energy_cost: int = EnergyActor.INSTANT
    file_name: str = ""

    def act(self, scene) -> None:
        """
        Execute the load game operation.

        This method is called by the energy system when this component's turn
        arrives in the action queue. It removes itself from the component manager
        to prevent state corruption and then calls load_world to perform the
        actual deserialization.

        Args:
            scene: The active game scene containing the component manager and
                  deserialization logic.

        Returns:
            None

        """
        scene.cm.delete_component(self)

        self.load_world(scene)

    def load_world(self, scene):
        """
        Load and deserialize the game state from the specified file.

        This method handles the actual deserialization process:
        1. It records the start time for performance tracking
        2. Loads the serialized data from the file using the scene's load_game method
        3. Passes the data to the component manager's from_data method to reconstruct
           all game objects
        4. Records the end time and logs performance statistics
        5. Provides user feedback through the scene messaging system

        Args:
            scene: The active game scene containing the component manager and
                  deserialization logic.

        Returns:
            None

        """
        start = core.time_ms()
        self._log_info(f"attempting to read game")
        data = scene.load_game(self.file_name)
        scene.cm.from_data(data)
        end = core.time_ms()
        self._log_info(f"loaded {len(data)} objects in {end - start}ms")
        scene.message(t("message.game_loaded"), color=palettes.LIGHT_WATER)
