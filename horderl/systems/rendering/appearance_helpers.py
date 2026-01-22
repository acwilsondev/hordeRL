from typing import Tuple, Union

from horderl import palettes
from horderl.components import Appearance

Color = Tuple[int, int, int]
PaletteColor = Union[Color, str]


def resolve_palette_color(color: PaletteColor) -> Color:
    """
    Resolve a palette color name or RGB tuple into an RGB tuple.

    Args:
        color: An RGB tuple or a palette attribute name.

    Returns:
        The resolved RGB tuple.

    Raises:
        ValueError: If the palette attribute name does not exist.
    """
    if isinstance(color, str):
        try:
            return getattr(palettes, color)
        except AttributeError as exc:
            raise ValueError(f"Unknown palette color '{color}'") from exc
    return color


def apply_palette_updates(appearance: Appearance) -> None:
    """
    Apply palette updates to an appearance in-place when palette keys are used.

    Args:
        appearance: The Appearance component to update.

    Side effects:
        - Mutates appearance.color and appearance.bg_color when they reference
          palette attribute names.
    """
    if isinstance(appearance.color, str):
        appearance.color = resolve_palette_color(appearance.color)
    if isinstance(appearance.bg_color, str):
        appearance.bg_color = resolve_palette_color(appearance.bg_color)


def appearance_to_tile(appearance: Appearance) -> tuple:
    """
    Convert an Appearance component into a tcod tile tuple.

    Args:
        appearance: The Appearance component to translate.

    Returns:
        A tcod tile tuple: (char, fg RGBA tuple, bg RGBA tuple).

    Side effects:
        - Applies palette updates to keep appearance colors current.
    """
    apply_palette_updates(appearance)
    return (
        ord(appearance.symbol),
        (*appearance.color, 255),
        (*appearance.bg_color, 255),
    )


def update_appearance(
    appearance: Appearance,
    symbol: str,
    fg: PaletteColor,
    bg: PaletteColor,
) -> None:
    """
    Update an Appearance component with new symbol and colors.

    Args:
        appearance: The Appearance component to update.
        symbol: The new glyph character.
        fg: The new foreground RGB tuple or palette attribute name.
        bg: The new background RGB tuple or palette attribute name.

    Side effects:
        - Mutates appearance.symbol, appearance.color, and appearance.bg_color.
        - Applies palette updates to keep appearance colors current.
    """
    appearance.symbol = symbol
    appearance.color = fg
    appearance.bg_color = bg
    apply_palette_updates(appearance)
