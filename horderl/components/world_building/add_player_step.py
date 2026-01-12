from dataclasses import dataclass

from horderl.components.events.build_world_events import BuildWorldListener

from ...content.player import make_player


@dataclass
class AddPlayerStep(BuildWorldListener):
    def on_build_world(self, scene):
        self._log_info(f"adding player to map")
        player = make_player(
            scene.config.map_height // 2,
            scene.config.map_width // 2,
            scene.config,
        )
        scene.cm.add(*player[1])
