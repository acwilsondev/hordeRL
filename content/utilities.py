from components import Entity
from components.attack_start_listeners.move_peasants_in import MovePeasantsIn
from components.season_reset_listeners.add_villager import AddVillager
from components.actors.calendar_actor import Calendar
from components.season_reset_listeners.collect_taxes import CollectTaxes
from components.season_reset_listeners.move_peasants_out import MovePeasantsOut
from components.season_reset_listeners.reset_health import ResetHealth
from engine import core


def make_calendar():
    entity_id = core.get_id('calendar')
    return [
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name='calendar'),
            Calendar(entity=entity_id),
            ResetHealth(entity=entity_id),
            CollectTaxes(entity=entity_id),
            AddVillager(entity=entity_id),
            MovePeasantsOut(entity=entity_id),
            MovePeasantsIn(entity=entity_id)
        ]
    ]
