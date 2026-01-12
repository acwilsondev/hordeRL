import json
import logging

import pytest

yaml = pytest.importorskip("yaml")

from horderl.config import CONFIG_VERSION, load_config


def test_load_config_creates_options_file(tmp_path):
    options_path = tmp_path / "options.yaml"

    config = load_config(str(options_path), overrides={})

    assert options_path.exists()
    assert config.character_name == "Sir Cameron"
    assert config.color_background == (0, 0, 0)
    assert config.map_width == config.screen_width - 25

    options_data = yaml.safe_load(options_path.read_text())
    assert options_data["config_version"] == CONFIG_VERSION
    assert "color_background" not in options_data


def test_load_config_merges_overrides(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(
        yaml.safe_dump(
            {
                "character-name": "Sir Test",
                "grass-density": 0.2,
            }
        )
    )

    config = load_config(
        str(options_path),
        overrides={"character_name": "Overridden", "grass_density": 0.3},
    )

    assert config.character_name == "Overridden"
    assert config.grass_density == 0.3


def test_load_config_rejects_invalid_types(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(yaml.safe_dump({"grass-density": "loud"}))

    try:
        load_config(str(options_path), overrides={})
    except ValueError as exc:
        assert "grass_density" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid grass density")


def test_load_config_ignores_color_overrides(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(yaml.safe_dump({"color_background": "ffffff"}))

    config = load_config(str(options_path), overrides={})

    assert config.color_background == (0, 0, 0)


def test_load_config_applies_color_palette(tmp_path):
    options_path = tmp_path / "options.yaml"
    palette_path = tmp_path / "palette.json"
    palette_path.write_text(
        json.dumps(
            {
                "color_background": "ffffff",
                "grass": [1, 2, 3],
            }
        )
    )
    options_path.write_text(
        yaml.safe_dump({"color-palette": str(palette_path)})
    )

    config = load_config(str(options_path), overrides={})

    assert config.color_background == (255, 255, 255)
    assert config.color_grass == (1, 2, 3)


def test_load_config_accepts_hash_color_values(tmp_path):
    options_path = tmp_path / "options.yaml"
    palette_path = tmp_path / "palette.json"
    palette_path.write_text(json.dumps({"color_background": "#282828"}))
    options_path.write_text(
        yaml.safe_dump({"color-palette": str(palette_path)})
    )

    config = load_config(str(options_path), overrides={})

    assert config.color_background == (40, 40, 40)


def test_load_config_warns_on_invalid_palette(tmp_path, caplog):
    options_path = tmp_path / "options.yaml"
    palette_path = tmp_path / "palette.json"
    palette_path.write_text("")
    options_path.write_text(
        yaml.safe_dump({"color-palette": str(palette_path)})
    )

    with caplog.at_level(logging.WARNING):
        config = load_config(str(options_path), overrides={})

    assert config.color_background == (0, 0, 0)
    assert any(
        "Failed to load color palette" in record.message
        for record in caplog.records
    )
