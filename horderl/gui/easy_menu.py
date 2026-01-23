import textwrap
from typing import Callable, Optional

from engine import core
from engine.ui.gui_element import GuiElement

from .. import palettes
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
        super().__init__(0, 0)
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
        self.page = 0
        self.modal = True

    def update(self, scene, dt_ms: int) -> None:
        import tcod.event

        key_event = core.get_key_event()
        if key_event is None:
            return

        key_sym = int(key_event.sym)
        has_next = self.page + 1 < len(self.pages)
        has_previous = self.page > 0

        if key_sym == tcod.event.KeySym.RETURN:
            self.close()
            return
        if self.on_escape and key_sym == tcod.event.KeySym.ESCAPE:
            self.on_escape()
            self.close()
            return
        if self.return_only:
            return
        nav_actions = {
            tcod.event.KeySym.RIGHT: has_next,
            tcod.event.KeySym.n: has_next,
            tcod.event.KeySym.LEFT: has_previous,
            tcod.event.KeySym.p: has_previous,
        }
        if nav_actions.get(key_sym, False):
            delta = (
                1
                if key_sym in (tcod.event.KeySym.RIGHT, tcod.event.KeySym.n)
                else -1
            )
            self.page += delta
            return

        index = key_sym - ord("a")

        # adjust index for the correct page
        index += self.page * 10

        if 0 <= index < len(self.options):
            option_at_index = self.options[index]
            callback = self.option_map.get(
                option_at_index,
                lambda: print(t("menu.nav.no_option")),
            )
            callback()
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
        import tcod

        lines = textwrap.wrap(
            self.header,
            self.width,
            break_long_words=False,
            replace_whitespace=False,
        )
        header_height = len(lines)

        if not self.header:
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
        nav_text = None
        if has_next and has_previous:
            nav_text = t("menu.nav.previous_next")
        elif has_previous:
            nav_text = t("menu.nav.previous")
        elif has_next:
            nav_text = t("menu.nav.next")
        if nav_text:
            window.print(0, y, nav_text, fg=palettes.WHITE, bg=None)

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
