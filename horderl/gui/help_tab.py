from ..engine import palettes
from ..gui.gui_element import GuiElement


class HelpTab(GuiElement):
    """Represent a text label."""

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
        """Draw the bar onto the panel"""
        panel.print(
            self.x,
            self.y,
            "Controls_________________________",
            fg=self.fg,
            bg=self.bg,
        )
        panel.print(self.x, self.y + 1, "  ↑ ", fg=self.mg, bg=self.bg)
        panel.print(
            self.x, self.y + 2, "← ↓ →  : Move / Attack", fg=self.mg, bg=self.bg
        )

        panel.print(
            self.x, self.y + 4, "SPACE  : Use Ability", fg=self.mg, bg=self.bg
        )
        panel.print(
            self.x, self.y + 5, "q      : Last Ability", fg=self.mg, bg=self.bg
        )
        panel.print(
            self.x, self.y + 6, "e      : Next Ability", fg=self.mg, bg=self.bg
        )
        panel.print(self.x, self.y + 7, "ESC    : Back", fg=self.mg, bg=self.bg)
