from dataclasses import dataclass

from ..events.die_events import DeathListener
from ..events.terrain_changed_event import TerrainChangedEvent


@dataclass
class TerrainChangedOnDeath(DeathListener):
    """This entity is a part of the terrain and should notify anything that cares about terrain when it dies."""

    def on_die(self, scene):
        self._log_info("triggering, emitting TerrainChangedEvent")
        scene.cm.add(TerrainChangedEvent(entity=scene.player))
