from dataclasses import dataclass, field

from engine.components.component import Component


@dataclass
class Weather(Component):
    """Store weather state and configuration for the calendar."""

    temperature: int = 20
    seasonal_norm: int = 20
    daily_variation: int = 10
    seasonal_temperatures: dict[str, int] = field(
        default_factory=lambda: {
            "Spring": 20,
            "Summer": 30,
            "Fall": 10,
            "Winter": -5,
        }
    )
