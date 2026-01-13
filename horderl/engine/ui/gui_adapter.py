from typing import Any, Callable

from .gui import Gui


class GuiAdapter:
    def __init__(
        self,
        gui: Gui,
        popup_factory: Callable[[str, Any], Any] | None = None,
    ) -> None:
        self._gui = gui
        self._popup_factory = popup_factory

    @property
    def gui(self) -> Gui:
        return self._gui

    def clear_root(self) -> None:
        self._gui.root.clear()

    def render_element(self, element: Any) -> None:
        element.render(self._gui.root)

    def render_single_shot(self, element: Any) -> None:
        element.render(self._gui.root)

    def create_popup(self, message: str, config: Any) -> Any:
        if self._popup_factory is None:
            raise ValueError(
                "GuiAdapter requires a popup_factory to create popups."
            )
        return self._popup_factory(message, config)
