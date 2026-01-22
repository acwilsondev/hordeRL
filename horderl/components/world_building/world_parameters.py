import time
from dataclasses import dataclass, field

from engine.components.component import Component

DEFAULT_LAKES: int = 1
DEFAULT_LAKE_PROLIFERATION: float = 0.2
DEFAULT_COPSE: int = 10
DEFAULT_COPSE_PROLIFERATION: float = 0.05
DEFAULT_ROCKS: int = 2
DEFAULT_ROCKS_PROLIFERATION: float = 0.075
DEFAULT_FLOWERS: int = 10
DEFAULT_FLOWER_PROLIFERATION: float = 0.1
DEFAULT_TEMPERATURE_MODIFIER: int = 0
DEFAULT_RIVER_RAPIDS: int = 3000
DEFAULT_TREE_CUT_ANGER: int = 1


@dataclass
class WorldParameters(Component):
    """Data container describing parameters for world generation."""

    biome: str = "Plains"

    lakes: int = DEFAULT_LAKES
    lake_proliferation: float = DEFAULT_LAKE_PROLIFERATION

    copse: int = DEFAULT_COPSE
    copse_proliferation: float = DEFAULT_COPSE_PROLIFERATION

    rock_fields: int = DEFAULT_ROCKS
    rocks_proliferation: float = DEFAULT_ROCKS_PROLIFERATION

    flower_fields: int = DEFAULT_FLOWERS
    flower_proliferation: float = DEFAULT_FLOWER_PROLIFERATION

    temperature_modifier: int = DEFAULT_TEMPERATURE_MODIFIER

    is_water_swampy: bool = False
    river_rapids: int = DEFAULT_RIVER_RAPIDS

    # how much cutting a tree angers the nature spirit
    tree_cut_anger: int = DEFAULT_TREE_CUT_ANGER

    world_name: str = ""

    world_seed: int | str = field(default_factory=time.time_ns)

    flower_color = None

    def get_file_name(self) -> str:
        """Return a file-friendly world name derived from the title."""
        return self.world_name.replace(" ", "-")
