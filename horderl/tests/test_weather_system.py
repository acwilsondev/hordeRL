import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import core
from engine.component_manager import ComponentManager
from horderl.components.events.new_day_event import DayBegan
from horderl.components.events.start_game_events import StartGame
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.weather.weather import Weather
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.systems.weather_system import run as run_weather_system


class DummyScene:
    """Minimal scene stub exposing a component manager and message log."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager and message storage."""
        self.cm = ComponentManager()
        self.messages: list[str] = []

    def message(self, text: str, color=None) -> None:
        """Record message text so tests can assert weather notifications."""
        self.messages.append(text)


def test_weather_system_updates_temperature_on_day_began():
    scene = DummyScene()
    calendar_id = core.get_id("calendar")
    weather = Weather(
        entity=calendar_id,
        temperature=20,
        seasonal_norm=15,
        daily_variation=0,
    )
    scene.cm.add(weather, DayBegan(entity=calendar_id, day=1))

    run_weather_system(scene)

    assert weather.temperature == 15
    assert scene.messages == []


def test_weather_system_reports_freezing_on_season_reset(monkeypatch):
    scene = DummyScene()
    calendar_id = core.get_id("calendar")
    world_id = core.get_id("world")
    weather = Weather(entity=calendar_id, temperature=5, seasonal_norm=20)
    scene.cm.add(
        weather,
        WorldParameters(entity=world_id, temperature_modifier=0),
        ResetSeason(entity=calendar_id, season="Winter"),
    )

    monkeypatch.setattr(
        "horderl.systems.weather_system.random.randint", lambda a, b: 0
    )

    run_weather_system(scene)

    assert weather.seasonal_norm == -5
    assert weather.temperature == -5
    assert "It is freezing outside." in scene.messages


def test_weather_system_initializes_on_game_start(monkeypatch):
    scene = DummyScene()
    calendar_id = core.get_id("calendar")
    world_id = core.get_id("world")
    weather = Weather(entity=calendar_id, temperature=0, seasonal_norm=0)
    scene.cm.add(
        weather,
        WorldParameters(entity=world_id, temperature_modifier=5),
        StartGame(entity=calendar_id),
    )

    monkeypatch.setattr(
        "horderl.systems.weather_system.random.randint", lambda a, b: 0
    )

    run_weather_system(scene)

    assert weather.seasonal_norm == 25
    assert weather.temperature == 25
