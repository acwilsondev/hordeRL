from dataclasses import dataclass

from engine import core
from engine.components import EnergyActor
from engine.logging import get_logger
from horderl.components.actors.calendar_actor import Calendar
from horderl.components.events.new_day_event import DayBegan


@dataclass
class FastForward(EnergyActor):
    """
    Event actor that advances the calendar to a fixed day.

    This component fast-forwards the game calendar and triggers a new day event.
    """

    energy_cost: int = EnergyActor.INSTANT

    def act(self, scene):
        """
        Fast-forward the calendar and remove this component.

        Args:
            scene: Active scene containing component manager.

        Side Effects:
            - Updates calendar day and energy.
            - Emits a DayBegan event.
            - Removes the fast-forward component.
        """
        logger = get_logger(__name__)
        logger.debug(
            "Fast-forwarding calendar",
            extra={"entity": self.entity, "target_day": 30},
        )
        calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
        if calendar:
            calendar.day = 30
            calendar.energy = 0
            scene.cm.add(DayBegan(entity=core.get_id("calendar"), day=30))
        scene.cm.delete_component(self)
