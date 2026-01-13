import textwrap
from typing import Callable, Optional

from .. import palettes
from ..engine import core
from ..engine.ui.gui_element import GuiElement
from ..i18n import t


class EasyMenu(GuiElement):
    """
    Defines a multiple choice menu within the game.
    """

    def __init__(
        self,
        header,
        options,
        width,
        config,
        hide_background=True,
        return_only=False,
        on_escape=None,
    ):
        super().__init__(0, 0, single_shot=True)
        self.header = header
        self.option_map = options
        self.options = [o for o in options.keys()]
        self.width = width
        self.config = config
        self.pages = [
            self.options[i : i + 10] for i in range(0, len(self.options), 10)
        ]
        self.hide_background = hide_background
        self.return_only = return_only
        if len(self.pages) == 0:
            self.pages.append([])
        self.on_escape: Optional[Callable] = on_escape

    def render(self, panel):
        """
        Draw a menu to the screen and return the user's option.
        """
        import tcod
        import tcod.event

        page = 0
        index = None
        while index is None:
            has_next = page + 1 < len(self.pages)
            has_previous = page > 0
            key_event = self.show_and_get_input(
                panel,
                self.pages[page],
                has_next=has_next,
                has_previous=has_previous,
            )
            key_sym = int(key_event.sym)
            if (
                key_sym == tcod.event.KeySym.RIGHT
                or key_sym == tcod.event.KeySym.n
            ) and has_next:
                page += 1
            elif (
                key_sym == tcod.event.KeySym.LEFT
                or key_sym == tcod.event.KeySym.p
            ) and has_previous:
                page -= 1
            elif key_sym == tcod.event.KeySym.RETURN:
                return
            elif self.on_escape and key_sym == tcod.event.KeySym.ESCAPE:
                self.on_escape()
                return
            else:
                index = key_sym - ord("a")

                # adjust index for the correct page
                index += page * 10

                if 0 <= index < len(self.options):
                    option_at_index = self.options[index]
                    callback = self.option_map.get(
                        option_at_index,
                        lambda: print(t("menu.nav.no_option")),
                    )
                    callback()

    def show_and_get_input(
        self, root, options, has_next=False, has_previous=False
    ):
        import tcod
        from tcod import libtcodpy
        from tcod.event_constants import K_RETURN

        lines = textwrap.wrap(
            self.header,
            self.width,
            break_long_words=False,
            replace_whitespace=False,
        )
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
            window.print(1, 0 + i, lines[i], fg=palettes.WHITE, bg=None)

        y = header_height
        letter_index = ord("a")
        for option_text in options:
            text = "(" + chr(letter_index) + ") " + option_text
            window.print(0, y, text, fg=palettes.WHITE, bg=None)
            y += 1
            letter_index += 1

        # add nav
        if has_previous and not has_next:
            window.print(
                0, y, t("menu.nav.previous"), fg=palettes.WHITE, bg=None
            )
        elif has_next and not has_previous:
            window.print(0, y, t("menu.nav.next"), fg=palettes.WHITE, bg=None)
        elif has_next and has_previous:
            window.print(
                0,
                y,
                t("menu.nav.previous_next"),
                fg=palettes.WHITE,
                bg=None,
            )

        if self.hide_background:
            # Draw a blank screen
            background = tcod.console.Console(
                self.config.screen_width,
                self.config.screen_height,
                order="F",
            )
            background.draw_rect(
                0,
                0,
                self.config.screen_width,
                self.config.screen_height,
                0,
                bg=palettes.BACKGROUND,
            )
            background.blit(root)

        x = self.config.screen_width // 2 - self.width // 2
        y = self.config.screen_height // 2 - height // 2
        window.blit(root, x, y, width=self.width, height=height)

        libtcodpy.console_flush()

        key_event = core.wait_for_char()
        if self.return_only:
            while key_event is None or int(key_event.sym) != K_RETURN:
                key_event = core.wait_for_char()

        return key_event
