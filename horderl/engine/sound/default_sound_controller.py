import logging

from ...engine.sound.sound_controller import SoundController


class DefaultSoundController(SoundController):
    def __init__(self):
        logging.debug(
            "DefaultSoundController: sound has been removed from the game for now."
        )

    def play(self, track: str):
        pass


tracks = {
    "theme": "./resources/theme.ogg",
    "town": "./resources/town.ogg",
    "battle": "./resources/battle.ogg",
}
