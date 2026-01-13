import textwrap

import tcod
import tcod.event

from horderl.engine_adapter import GuiElement, core

from .. import palettes
from ..i18n import t


class Menu(GuiElement):
    """
    Defines a multiple choice menu within the game.
    """

    def __init__(self, header, options, width, callback, config):
        super().__init__(0, 0)
        self.header = header
        self.options = options
        self.width = width
        self.callback = callback
        self.config = config
        self.pages = [options[i : i + 10] for i in range(0, len(options), 10)]
        if len(self.pages) == 0:
            self.pages.append([])
        self.page = 0
        self.modal = True

    def update(self, scene, dt: float) -> None:
        key_event = core.get_key_event()
        if key_event is None:
            return

        key_sym = key_event.sym
        has_next = self.page + 1 < len(self.pages)
        has_previous = self.page > 0
        if (
            key_sym is tcod.event.KeySym.RIGHT or key_sym is tcod.event.K_n
        ) and has_next:
            self.page += 1
            return
        if (
            key_sym is tcod.event.KeySym.LEFT
            or key_sym is tcod.event.KeySym.p
        ) and has_previous:
            self.page -= 1
            return
        if key_sym is tcod.event.KeySym.RETURN:
            self.close()
            return

        index = key_sym - ord("a")

        # adjust index for the correct page
        index += self.page * 10

        if 0 <= index < len(self.options) and self.callback:
            self.callback(index)
            self.close()
            return
        if self.callback:
            self.callback(None)
            self.close()

    def render(self, panel):
        """
        Draw a menu to the screen.
        """
        self.draw_menu(
            panel,
            self.pages[self.page],
            has_next=self.page + 1 < len(self.pages),
            has_previous=self.page > 0,
        )

    def draw_menu(self, root, options, has_next=False, has_previous=False):
        lines = [
            "\n".join(
                textwrap.wrap(
                    line,
                    self.width,
                    break_long_words=False,
                    replace_whitespace=False,
                )
            )
            for line in self.header.splitlines()
            if line.strip() != ""
        ]
        header_height = len(lines)

        if self.header == "":
            header_height = 0
        height = len(options) + header_height
        if has_next:
            height += 1
        if has_previous:
            height += 1
        window = tcod.console.Console(self.width, height, order="F")
        window.draw_rect(
            0, 0, self.width, height, 0, fg=palettes.WHITE, bg=None
        )
        for i, _ in enumerate(lines):
            window.print(1, 0 + i, lines[i])

        y = header_height
        letter_index = ord("a")
        for option_text in options:
            text = "(" + chr(letter_index) + ") " + option_text
            window.print(0, y, text, bg=None)
            y += 1
            letter_index += 1

        # add nav
        if has_previous and not has_next:
            window.print(0, y, t("menu.nav.previous"), bg=None)
        elif has_next and not has_previous:
            window.print(0, y, t("menu.nav.next"), bg=None)
        elif has_next and has_previous:
            window.print(0, y, t("menu.nav.previous_next"), bg=None)

        x = self.config.screen_width // 2 - self.width // 2
        y = self.config.screen_height // 2 - height // 2
        window.blit(root, x, y, width=self.width, height=height)
