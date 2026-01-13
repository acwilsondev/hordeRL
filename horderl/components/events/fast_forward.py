from calendar import Calendar
from dataclasses import dataclass

from horderl.components.actors.calendar_actor import Calendar
from horderl.components.events.new_day_event import DayBegan
from horderl.engine import core
from horderl.components.actors.energy_actor import EnergyActor
from horderl.engine.core import log_debug


@dataclass
class FastForward(EnergyActor):
    energy_cost: int = EnergyActor.INSTANT

    @log_debug(__name__)
    def act(self, scene):
        calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
        if calendar:
            calendar.day = 30
            calendar.energy = 0
            scene.cm.add(DayBegan(entity=core.get_id("calendar"), day=30))
        scene.cm.delete_component(self)
