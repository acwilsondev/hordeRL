import time
from engine.components import Coordinates

from engine.ui.gui_element import GuiElement

from .. import palettes
from ..gui.labels import Label


class PositionTracker(GuiElement):
    """
    Automatically monitor FPS with a label.
    """

    def __init__(self, x, y, entity):
        super().__init__(x, y)
        self.last_update = time.time()
        self.entity = entity
        self.label = Label(x, y, "", fg=palettes.GOLD)

    def update(self, scene, dt: float):
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        if coords:
            self.label.value = f"({coords.x}, {coords.y})"
        else:
            self.label.value = "Player not found"

    def render(self, panel):
        self.label.render(panel)
