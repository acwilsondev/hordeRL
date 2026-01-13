from dataclasses import dataclass

from engine.ui.gui_element import GuiElement

from ..gui.easy_menu import EasyMenu


@dataclass
class PopupMessage(GuiElement):
    def __init__(self, message, config):
        super().__init__(0, 0, name=message, single_shot=True)
        self.menu = EasyMenu(
            message + " [ENTER]",
            {},
            config.inventory_width,
            config,
            return_only=True,
        )

    def render(self, panel):
        self.menu.render(panel)
