import tcod.console
from tcod import libtcodpy

import settings


class Gui:
    """Represent the engine's GUI"""

    def __init__(self, width=0, height=0, title=''):
        libtcodpy.console_set_custom_font(
            settings.FONT,
            libtcodpy.FONT_LAYOUT_CP437 | libtcodpy.FONT_TYPE_GREYSCALE,
        )
        self.root = libtcodpy.console_init_root(
            width,
            height,
            title=title,
            order="F",
            renderer=libtcodpy.RENDERER_SDL2
        )
        self.gui_elements = set()

    def add_element(self, element):
        if element.single_shot:
            # if it's a single shot (menu or popup message), we need to render it directly to the existing window
            self.root.clear()
            element.render(self.root)
        else:
            self.gui_elements.add(element)

    def tear_down(self):
        self.gui_elements.clear()

    def close(self):
        self.root.__exit__()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
