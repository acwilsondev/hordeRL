from horderl.gui.gui import Gui
from horderl.gui.popup_message import PopupMessage


class GuiAdapter:
    def __init__(self, gui: Gui) -> None:
        self._gui = gui

    @property
    def gui(self) -> Gui:
        return self._gui

    def clear_root(self) -> None:
        self._gui.root.clear()

    def render_element(self, element) -> None:
        element.render(self._gui.root)

    def render_single_shot(self, element) -> None:
        self._gui.root.clear()
        element.render(self._gui.root)

    def create_popup(self, message: str, config):
        return PopupMessage(message, config)
