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


def test_load_config_merges_overrides(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(
        yaml.safe_dump({
            "character-name": "Sir Test",
            "grass-density": 0.2,
            "color_background": "ffffff",
        })
    )

    config = load_config(
        str(options_path),
        overrides={"character_name": "Overridden", "grass_density": 0.3},
    )

    assert config.character_name == "Overridden"
    assert config.grass_density == 0.3
    assert config.color_background == (255, 255, 255)


def test_load_config_rejects_invalid_types(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(yaml.safe_dump({"grass-density": "loud"}))

    try:
        load_config(str(options_path), overrides={})
    except ValueError as exc:
        assert "grass_density" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid grass density")


def test_load_config_accepts_color_list(tmp_path):
    options_path = tmp_path / "options.yaml"
    options_path.write_text(yaml.safe_dump({"color_background": [1, 2, 3]}))

    config = load_config(str(options_path), overrides={})

    assert config.color_background == (1, 2, 3)
