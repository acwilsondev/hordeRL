from typing import List

from horderl.components import Appearance, Attributes, Coordinates
from horderl.components.brains.peasant_actor import PeasantActor
from horderl.components.cry_for_help import CryForHelp
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.death_listeners.on_die_emit_peasant_died import (
    OnDieEmitPeasantDied,
)
from horderl.components.edible import Edible
from horderl.components.events.peasant_events import PeasantAdded
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.movement.move import Move
from horderl.components.pathfinding.peasant_cost_mapper import (
    PeasantCostMapper,
)
from horderl.components.relationships.residence import Residence
from horderl.components.tags.peasant_tag import PeasantTag
from horderl.components.target_value import PEASANT, TargetValue
from horderl.engine import core, palettes
from horderl.engine.components.component import Component
from horderl.engine.components.entity import Entity
from horderl.engine.constants import PRIORITY_MEDIUM
from horderl.engine.types import EntityId

peasant_description = (
    "A peasant, tasked with working the fields. "
    "Unaware of your incompetency, their face belies a cheerful contentment."
)


def make_peasant(house_id, x, y) -> Entity:
    entity_id: EntityId = core.get_id()
    components: List[Component] = [
        Entity(
            id=entity_id,
            entity=entity_id,
            name="peasant",
            description=peasant_description,
        ),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
        Faction(entity=entity_id, faction=Faction.Options.PEASANT),
        PeasantTag(entity=entity_id),
        Appearance(
            entity=entity_id,
            symbol="p",
            color=palettes.WHITE,
            bg_color=palettes.BACKGROUND,
        ),
        Corpse(entity=entity_id),
        Attributes(entity=entity_id, hp=10, max_hp=10),
        TargetValue(entity=entity_id, value=PEASANT),
        Material(entity=entity_id, blocks=False, blocks_sight=False),
        CryForHelp(entity=entity_id),
        Residence(entity=entity_id, house_id=house_id),
        Move(entity=entity_id),
        Edible(entity=entity_id, sleep_for=20),
        PeasantActor(entity=entity_id),
        PeasantAdded(entity=entity_id),
        OnDieEmitPeasantDied(entity=entity_id),
        PeasantCostMapper(entity=entity_id),
    ]
    return entity_id, components
