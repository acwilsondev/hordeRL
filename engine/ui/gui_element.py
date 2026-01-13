from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tcod

from ..core import get_id


@dataclass
class GuiElement:
    """
    Form the base behavior of a GuiElement.
    """

    x: int = 0
    y: int = 0
    name: str = ""
    id: int = field(default_factory=get_id)
    # if true, the GUI won't store this element, but will render it immediately
    single_shot: bool = False
    modal: bool = False
    is_closed: bool = False

    def on_load(self) -> None:
        """
        Perform any actions necessary before rendering.

        Called while pushing the scene, after the scene's on_load method.

        """

    def update(self, scene, dt: float) -> None:
        pass

    def render(self, panel: "tcod.console.Console") -> None:
        raise NotImplementedError("GuiElement must define render()")

    def close(self) -> None:
        self.is_closed = True
