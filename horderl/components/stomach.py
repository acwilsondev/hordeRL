from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class Stomach(Component):
    """Track an entity stored inside another entity."""

    contents: int = constants.INVALID

    def clear(self, scene):
        """
        Drop the currently stored entity from the component manager stash.

        Args:
            scene: Scene providing the component manager used to drop the stash.

        Side Effects:
            - Removes the stashed entity and resets stored contents to INVALID.
        """
        if self.contents == constants.INVALID:
            return

        self._log_debug(f"clearing contents {self.contents}")
        scene.cm.drop_stashed_entity(self.contents)
        self.contents = constants.INVALID
