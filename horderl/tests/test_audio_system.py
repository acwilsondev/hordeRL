from engine.component_manager import ComponentManager
from horderl.components.events.attack_started_events import AttackStarted
from horderl.components.events.start_game_events import StartGame
from horderl.components.sound.battle_music import BattleMusic
from horderl.components.sound.start_music import StartMusic
from horderl.systems.audio_system import run as run_audio_system


class DummySound:
    def __init__(self):
        self.played = []

    def play(self, track_id: str) -> None:
        self.played.append(track_id)


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.sound = DummySound()


def test_audio_system_plays_start_music_on_start_game_event():
    scene = DummyScene()

    scene.cm.add(StartMusic(entity=1), StartGame(entity=1))

    run_audio_system(scene)

    assert scene.sound.played == ["town"]


def test_audio_system_plays_battle_music_on_attack_started():
    scene = DummyScene()

    scene.cm.add(BattleMusic(entity=1), AttackStarted(entity=1))

    run_audio_system(scene)

    assert scene.sound.played == ["battle"]
