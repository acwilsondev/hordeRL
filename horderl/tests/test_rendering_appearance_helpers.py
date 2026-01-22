from horderl import palettes
from horderl.components import Appearance
from horderl.systems.rendering.appearance_helpers import (
    appearance_to_tile,
    update_appearance,
)


def test_appearance_to_tile_resolves_palette_names():
    appearance = Appearance(
        symbol="@",
        color="DEBUG",
        bg_color="BACKGROUND",
    )

    tile = appearance_to_tile(appearance)

    assert tile == (
        ord("@"),
        (*palettes.DEBUG, 255),
        (*palettes.BACKGROUND, 255),
    )
    assert appearance.color == palettes.DEBUG
    assert appearance.bg_color == palettes.BACKGROUND


def test_update_appearance_applies_palette_colors():
    appearance = Appearance(symbol="a", color=palettes.WHITE)

    update_appearance(appearance, "*", "DEBUG", "BACKGROUND")

    assert appearance.symbol == "*"
    assert appearance.color == palettes.DEBUG
    assert appearance.bg_color == palettes.BACKGROUND
