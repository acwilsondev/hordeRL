from ..engine import palettes
from ..gui.gui_element import GuiElement
from ..i18n import t


class HelpTab(GuiElement):
    """
    Represent a text label.
    """

    def __init__(
        self,
        x,
        y,
        fg=palettes.WHITE,
        mg=palettes.MEAT,
        bg=palettes.BACKGROUND,
        name=None,
    ):
        super().__init__(x, y, name=name)
        self.fg = fg
        self.mg = mg
        self.bg = bg

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(
            self.x,
            self.y,
            t("help.controls_title"),
            fg=self.fg,
            bg=self.bg,
        )
        panel.print(self.x, self.y + 1, "  ↑ ", fg=self.mg, bg=self.bg)
        panel.print(
            self.x,
            self.y + 2,
            t("help.move_attack"),
            fg=self.mg,
            bg=self.bg,
        )

        panel.print(
            self.x,
            self.y + 4,
            t("help.use_ability"),
            fg=self.mg,
            bg=self.bg,
        )
        panel.print(
            self.x,
            self.y + 5,
            t("help.last_ability"),
            fg=self.mg,
            bg=self.bg,
        )
        panel.print(
            self.x,
            self.y + 6,
            t("help.next_ability"),
            fg=self.mg,
            bg=self.bg,
        )
        panel.print(
            self.x,
            self.y + 7,
            t("help.back"),
            fg=self.mg,
            bg=self.bg,
        )
