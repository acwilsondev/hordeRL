import random
from engine.components import Coordinates

from engine import core
from engine.components.entity import Entity
from engine.constants import PRIORITY_MEDIUM
from horderl import palettes
from horderl.components import Appearance, Attributes
from horderl.components.attacks.standard_attack import StandardAttack
from horderl.components.brains.default_active_actor import DefaultActiveActor
from horderl.components.death_listeners.drop_gold import DropGold
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.movement.move import Move
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.pathfinding.stealthy_cost_map import StealthyCostMapper
from horderl.components.pathfinding.target_evaluation.hordeling_target_evaluator import (
    HordelingTargetEvaluator,
)
from horderl.components.stomach import Stomach
from horderl.components.tags.hordeling_tag import HordelingTag

description = "This shadowy creature lurks just out of sight."


def make_sneaker(x, y):
    entity_id = core.get_id()

    components = [
        Entity(id=entity_id, entity=entity_id, name="sneaky hordeling"),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
        Faction(entity=entity_id, faction=Faction.Options.MONSTER),
        Corpse(entity=entity_id),
        DefaultActiveActor(entity=entity_id),
        Appearance(
            entity=entity_id,
            symbol="s",
            color=palettes.HORDELING,
            bg_color=palettes.BACKGROUND,
            render_mode=Appearance.RenderMode.STEALTHY,
        ),
        Attributes(entity=entity_id, hp=1, max_hp=1),
        StandardAttack(entity=entity_id, damage=1),
        Material(entity=entity_id, blocks=True, blocks_sight=False),
        HordelingTag(entity=entity_id),
        Move(entity=entity_id),
        PathfinderCost(entity=entity_id, cost=5),
        StealthyCostMapper(entity=entity_id),
        Stomach(entity=entity_id),
        HordelingTargetEvaluator(entity=entity_id),
    ]

    if random.randint(1, 10) == 10:
        components.append(DropGold(entity=entity_id))

    return (entity_id, components)
