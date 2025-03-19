from horderl.engine.logging import get_logger
from horderl.engine.sound.sound_controller import SoundController


class DefaultSoundController(SoundController):
    def __init__(self):
        self.logger = get_logger(
            __name__, {"component": "DefaultSoundController"}
        )
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


tracks = {
    "theme": "./resources/theme.ogg",
    "town": "./resources/town.ogg",
    "battle": "./resources/battle.ogg",
}
