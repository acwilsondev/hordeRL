from dataclasses import dataclass

from horderl.engine_adapter import GuiElement

from ..gui.easy_menu import EasyMenu


@dataclass
class PopupMessage(GuiElement):
    def __init__(self, message, config):
        super().__init__(0, 0, name=message)
        self.menu = EasyMenu(
            message + " [ENTER]",
            {},
            config.inventory_width,
            config,
            return_only=True,
        )
        self.modal = True

    def update(self, scene, dt: float) -> None:
        self.menu.update(scene, dt)
        if self.menu.is_closed:
            self.close()

    def render(self, panel):
        self.menu.render(panel)
