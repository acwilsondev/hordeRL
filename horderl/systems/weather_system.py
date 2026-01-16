"""System that updates weather state in response to calendar events."""

from __future__ import annotations

import random
from typing import Iterable, List, TypeVar

from engine import GameScene, core
from horderl.components.events.new_day_event import DayBegan
from horderl.components.events.start_game_events import StartGame
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.weather.weather import Weather
from horderl.components.world_building.world_parameters import WorldParameters


def run(scene: GameScene) -> None:
    """
    Update weather state based on queued calendar events.

    Args:
        scene: Active game scene with the component manager and messaging.

    Side Effects:
        - Updates the Weather component's seasonal norm and temperature.
        - Sends a message if the temperature crosses freezing.

    """
    weather = _get_weather(scene)
    if not weather:
        return

    if scene.cm.get(StartGame):
        _set_seasonal_norm(scene, weather, "Spring")

    for season_event in _calendar_events(scene.cm.get(ResetSeason)):
        _set_seasonal_norm(scene, weather, season_event.season)

    for day_event in _calendar_events(scene.cm.get(DayBegan)):
        _set_temperature(scene, weather)


EventType = TypeVar("EventType")


def _calendar_events(events: Iterable[EventType]) -> List[EventType]:
    calendar_id = core.get_id("calendar")
    return [event for event in events if event.entity == calendar_id]


def _get_weather(scene: GameScene) -> Weather | None:
    # Weather is expected to be stored on the calendar entity.
    return scene.cm.get_one(Weather, entity=core.get_id("calendar"))


def _set_seasonal_norm(
    scene: GameScene, weather: Weather, season: str
) -> None:
    seasonal_temp = weather.seasonal_temperatures[season]
    world_params = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    modifier = world_params.temperature_modifier if world_params else 0
    weather.seasonal_norm = seasonal_temp + modifier
    weather._log_info(f"set normal temp {weather.seasonal_norm}")
    _set_temperature(scene, weather)


def _set_temperature(scene: GameScene, weather: Weather) -> None:
    previous_temp = weather.temperature
    weather.temperature = weather.seasonal_norm + random.randint(
        -weather.daily_variation, weather.daily_variation
    )
    weather._log_info(f"set daily temp {weather.temperature}")
    _notify_freezing_threshold(scene, previous_temp, weather.temperature)


def _notify_freezing_threshold(
    scene: GameScene, previous_temp: int, current_temp: int
) -> None:
    if previous_temp >= 0 > current_temp:
        scene.message("It is freezing outside.")
    elif previous_temp <= 0 < current_temp:
        scene.message("The weather warmed up.")
