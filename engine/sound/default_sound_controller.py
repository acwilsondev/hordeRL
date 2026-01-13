from typing import Mapping

from engine.logging import get_logger
from engine.sound.sound_controller import SoundController


class DefaultSoundController(SoundController):
    def __init__(self, tracks: Mapping[str, str]):
        self.logger = get_logger(
            __name__, {"component": "DefaultSoundController"}
        )
        self.tracks = dict(tracks)
        self.logger.debug(
            "Sound system initialized in disabled mode",
            extra={
                "status": "disabled",
                "reason": "sound temporarily removed",
            },
        )
        self.logger.info("Sound controller initialized")

    def play(self, track: str):
        self.logger.debug(
            f"Ignoring request to play track",
            extra={"track": track, "action": "play", "status": "skipped"},
        )
