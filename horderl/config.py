import json
import logging
import os
import struct
import sys
from dataclasses import dataclass, field, fields
from typing import Any, Dict

CONFIG_VERSION = 1
MIN_SCREEN_TILES = 50
MAX_SCREEN_TILES = 100

logger = logging.getLogger(__name__)


def resource_path(relative_path: str) -> str:
    """Return a path to packaged resources, supporting PyInstaller bundles."""
    try:
        # required for accessing resources within pyinstaller executable
        # noinspection PyProtectedMember,PyUnresolvedReferences
        base_path = sys._MEIPASS
    except AttributeError:
        # sys._MEIPASS only exists within python compiled for pyinstaller executables
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_relative_path(relative_path: str) -> str:
    """Return a path relative to the horderl package directory."""
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def from_hex(hex_code: str) -> tuple[int, int, int]:
    """Convert a hex RGB string into an (R, G, B) tuple."""
    return struct.unpack("BBB", bytes.fromhex(hex_code))


def _default_option_values() -> Dict[str, Any]:
    return {
        "autosave-enabled": True,
        "character-name": "Sir Cameron",
        "locale": "en",
        "grass-density": 0.1,
        "torch-radius": -1,
        "music-enabled": True,
        "world_seed": "RANDOM",
        "color-palette": "default",
        "screen-width": 60,
        "screen-height": 40,
        "log-environment": "development",
        "log-level": "INFO",
        "log-dir": "logs",
        "log-file": "horderl.log",
        "log-console-enabled": False,
        "config_version": CONFIG_VERSION,
    }


@dataclass
class Config:
    """Runtime configuration values for the game."""

    autosave_enabled: bool = True
    character_name: str = "Sir Cameron"
    locale: str = "en"
    grass_density: float = 0.1
    torch_radius: int = -1
    music_enabled: bool = True
    world_seed: str = "RANDOM"
    color_palette: str | None = "default"

    color_background: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("000000")
    )
    color_grass: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("1f240a")
    )
    color_wall_tree: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("39571c")
    )
    color_normal_tree: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("a58c27")
    )
    color_gold: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("efac28")
    )
    color_white: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("efd8a1")
    )
    color_peasant: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("ab5c1c")
    )
    color_shadow: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("183f39")
    )
    color_fire: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("ef692f")
    )
    color_straw: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("efb775")
    )
    color_dirt: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("a56243")
    )
    color_wood: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("773421")
    )
    color_meat: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("684c3c")
    )
    color_stone: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("927e6a")
    )
    color_water: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("276468")
    )
    color_fresh_blood: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("ef3a0c")
    )
    color_light_water: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("3c9f9c")
    )
    color_hordeling: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("9b1a0a")
    )
    color_blood: tuple[int, int, int] = field(
        default_factory=lambda: from_hex("550f0a")
    )

    font: str = field(
        default_factory=lambda: resource_path("resources/tiles.png")
    )
    screen_width: int = 60
    screen_height: int = 40
    map_width: int | None = None
    map_height: int | None = None
    bar_width: int = 20
    panel_height: int = 7
    panel_y: int | None = None
    msg_x: int | None = None
    msg_width: int | None = None
    msg_height: int | None = None
    inventory_width: int = 50

    fov_algo: str = "BASIC"
    fov_light_walls: bool = True
    spawn_frequency: int = 15
    log_environment: str = "development"
    log_level: str = "INFO"
    log_dir: str = "logs"
    log_file: str | None = "horderl.log"
    log_console_enabled: bool = False
    config_version: int = CONFIG_VERSION

    def __post_init__(self) -> None:
        self.map_width = (
            self.screen_width - 25
            if self.map_width is None
            else self.map_width
        )
        self.map_height = (
            self.screen_height if self.map_height is None else self.map_height
        )
        self.panel_y = (
            self.screen_height - self.panel_height
            if self.panel_y is None
            else self.panel_y
        )
        self.msg_x = self.bar_width + 2 if self.msg_x is None else self.msg_x
        self.msg_width = (
            self.screen_width - self.bar_width - 2
            if self.msg_width is None
            else self.msg_width
        )
        self.msg_height = (
            self.panel_height - 1
            if self.msg_height is None
            else self.msg_height
        )

        for field_name in _COLOR_FIELDS:
            value = getattr(self, field_name)
            if isinstance(value, str):
                setattr(self, field_name, from_hex(value))


_COLOR_FIELDS = [
    "color_background",
    "color_grass",
    "color_wall_tree",
    "color_normal_tree",
    "color_gold",
    "color_white",
    "color_peasant",
    "color_shadow",
    "color_fire",
    "color_straw",
    "color_dirt",
    "color_wood",
    "color_meat",
    "color_stone",
    "color_water",
    "color_fresh_blood",
    "color_light_water",
    "color_hordeling",
    "color_blood",
]

_OPTIONS_FIELD_MAP = {
    "autosave-enabled": "autosave_enabled",
    "character-name": "character_name",
    "locale": "locale",
    "grass-density": "grass_density",
    "torch-radius": "torch_radius",
    "music-enabled": "music_enabled",
    "world_seed": "world_seed",
    "color-palette": "color_palette",
    "screen-width": "screen_width",
    "screen-height": "screen_height",
    "log-environment": "log_environment",
    "log-level": "log_level",
    "log-dir": "log_dir",
    "log-file": "log_file",
    "log-console-enabled": "log_console_enabled",
    "config_version": "config_version",
}

_CONFIG_FIELDS = {field_info.name for field_info in fields(Config)}


def _normalize_options(values: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in values.items():
        normalized[_OPTIONS_FIELD_MAP.get(key, key)] = value
    return normalized


def _validate_types(values: Dict[str, Any]) -> None:
    expected_types = {
        "autosave_enabled": bool,
        "character_name": str,
        "locale": str,
        "grass_density": (int, float),
        "torch_radius": int,
        "music_enabled": bool,
        "world_seed": str,
        "color_palette": str,
        "font": str,
        "screen_width": int,
        "screen_height": int,
        "map_width": int,
        "map_height": int,
        "bar_width": int,
        "panel_height": int,
        "panel_y": int,
        "msg_x": int,
        "msg_width": int,
        "msg_height": int,
        "inventory_width": int,
        "fov_algo": str,
        "fov_light_walls": bool,
        "spawn_frequency": int,
        "log_environment": str,
        "log_level": str,
        "log_dir": str,
        "log_file": (str, type(None)),
        "log_console_enabled": bool,
        "config_version": int,
    }
    for color_field in _COLOR_FIELDS:
        expected_types[color_field] = (str, tuple, list)

    for field_name, expected in expected_types.items():
        if field_name not in values:
            continue
        value = values[field_name]
        if value is None:
            continue
        if not isinstance(value, expected):
            raise ValueError(
                f"Invalid type for {field_name}: expected {expected}, got"
                f" {type(value)}"
            )


def _validate_screen_dimensions(values: Dict[str, Any]) -> None:
    # Enforce positive screen sizes and warn on temporary limits.
    for dimension in ("screen_width", "screen_height"):
        value = values.get(dimension)
        if value is None:
            continue
        if value <= 0:
            raise ValueError(
                f"{dimension} must be greater than 0, got {value}"
            )
        if value < MIN_SCREEN_TILES or value > MAX_SCREEN_TILES:
            logger.warning(
                "%s is outside the supported range (%d-%d): %d",
                dimension,
                MIN_SCREEN_TILES,
                MAX_SCREEN_TILES,
                value,
            )


def _parse_color(value: Any) -> Any:
    if isinstance(value, str):
        normalized = value.lstrip("#")
        return from_hex(normalized)
    if isinstance(value, list):
        return tuple(value)
    return value


def _normalize_palette_key(key: str) -> str | None:
    normalized = key.replace("-", "_")
    if normalized in _COLOR_FIELDS:
        return normalized
    if not normalized.startswith("color_"):
        candidate = f"color_{normalized}"
        if candidate in _COLOR_FIELDS:
            return candidate
    return None


def _is_color_override_key(key: str) -> bool:
    return key.replace("-", "_") in _COLOR_FIELDS


def _resolve_palette_path(palette_name: str) -> str:
    if os.path.isfile(palette_name):
        return palette_name
    filename = palette_name
    if not filename.endswith(".json"):
        filename = f"{filename}.json"
    return resource_path(os.path.join("resources", "colors", filename))


def _load_palette(palette_name: str) -> Dict[str, Any]:
    palette_path = _resolve_palette_path(palette_name)
    if not os.path.exists(palette_path):
        raise FileNotFoundError(
            f"Color palette not found: {palette_name} ({palette_path})"
        )
    with open(palette_path, encoding="utf-8") as palette_file:
        palette_data = json.load(palette_file)
    if not isinstance(palette_data, dict):
        raise ValueError("Palette data must be a JSON object")
    if isinstance(palette_data.get("colors"), dict):
        palette_data = palette_data["colors"]
    if not isinstance(palette_data, dict):
        raise ValueError("Palette colors must be a JSON object")
    palette_colors = {}
    for key, value in palette_data.items():
        normalized_key = _normalize_palette_key(key)
        if normalized_key is None:
            continue
        palette_colors[normalized_key] = _parse_color(value)
    if not palette_colors:
        raise ValueError(f"Palette {palette_name} did not define any colors")
    return palette_colors


def _ensure_options_file(
    options_path: str, defaults: Dict[str, Any]
) -> Dict[str, Any]:
    import yaml

    if os.path.exists(options_path):
        return defaults

    options_dir = os.path.dirname(options_path)
    if options_dir:
        os.makedirs(options_dir, exist_ok=True)
    with open(options_path, mode="w", encoding="utf-8") as file:
        yaml.safe_dump(defaults, file, sort_keys=False)
    return defaults


def load_config(
    options_path: str, overrides: Dict[str, Any] | None = None
) -> Config:
    """Load configuration from defaults, options.yaml, and CLI overrides."""
    import yaml

    overrides = overrides or {}
    defaults = _default_option_values()
    strip_color_overrides = lambda data: (
        {
            key: value
            for key, value in data.items()
            if not _is_color_override_key(key)
        }
        if data
        else {}
    )

    if os.path.exists(options_path):
        with open(options_path, encoding="utf-8") as options_file:
            option_data = yaml.safe_load(options_file) or {}
        if not isinstance(option_data, dict):
            raise ValueError("options.yaml must contain a mapping")
    else:
        option_data = _ensure_options_file(options_path, defaults)

    option_data = strip_color_overrides(option_data)
    overrides = strip_color_overrides(overrides)

    merged = {
        **defaults,
        **option_data,
        **{k: v for k, v in overrides.items() if v is not None},
    }

    normalized = _normalize_options(merged)
    palette_name = normalized.get("color_palette")
    if palette_name not in (None, "default"):
        palette_path = _resolve_palette_path(palette_name)
        try:
            palette_colors = _load_palette(palette_name)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            logger.warning(
                "Failed to load color palette '%s' from '%s': %s. Falling back to default.",
                palette_name,
                palette_path,
                exc,
            )
        else:
            for key, value in palette_colors.items():
                normalized[key] = value
    normalized = {
        key: _parse_color(value) if key in _COLOR_FIELDS else value
        for key, value in normalized.items()
        if key in _CONFIG_FIELDS
    }

    _validate_types(normalized)
    _validate_screen_dimensions(normalized)

    return Config(**normalized)
