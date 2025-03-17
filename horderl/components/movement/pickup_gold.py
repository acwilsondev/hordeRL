from .. import Coordinates
from ..events.step_event import StepListener
from ..pickup_gold import GoldPickup
from ...engine import palettes


class PickupGoldOnStep(StepListener):
    """Whenever the owning entity takes a step into a gold containing square, pick it up."""

    def on_step(self, scene, point):
        self._log_debug("checking for gold at new location")
        for event in scene.cm.get(GoldPickup):
            gold_coords = scene.cm.get_one(Coordinates, entity=event.entity)
            if gold_coords.is_at_point(point):
                scene.cm.delete(event.entity)
                scene.gold += event.amount
                scene.message(f"You found {event.amount} gold.", color=palettes.GOLD)
