"""System for issuing audio playback commands based on queued events."""

from typing import Iterable, List

from engine import GameScene
from horderl.components.events.attack_started_events import AttackStarted
from horderl.components.events.start_game_events import StartGame
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.sound.battle_music import BattleMusic
from horderl.components.sound.start_music import StartMusic


def run(scene: GameScene) -> None:
    """
    Trigger music playback for queued game events.

    Args:
        scene: Active game scene containing component manager and sound IO.

    Side Effects:
        - Plays configured audio tracks via the scene sound subsystem.
    """
    if scene.cm.get(StartGame) or scene.cm.get(ResetSeason):
        _play_tracks(scene, scene.cm.get(StartMusic))

    if scene.cm.get(AttackStarted):
        _play_tracks(scene, scene.cm.get(BattleMusic))


def _play_tracks(scene: GameScene, components: Iterable) -> None:
    # Avoid duplicate playback for repeated track entries.
    tracks: List[str] = []
    seen = set()
    for component in components:
        if component.track_id not in seen:
            seen.add(component.track_id)
            tracks.append(component.track_id)

    for track_id in tracks:
        scene.sound.play(track_id)
