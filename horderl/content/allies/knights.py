from engine import core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.constants import PRIORITY_MEDIUM
from horderl import palettes
from horderl.components import Appearance, Attributes
from horderl.components.attacks.standard_attack import StandardAttack
from horderl.components.brains.stationary_attack_actor import (
    StationaryAttackActor,
)
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.pathfinding.normal_cost_mapper import NormalCostMapper
from horderl.components.pathfinding.target_evaluation.target_evaluator import (
    TargetEvaluator,
    TargetEvaluatorType,
from horderl.components.pathfinding.cost_mapper import (
    CostMapper,
    CostMapperType,
)
from horderl.components.sellable import Sellable
from horderl.components.tax_value import TaxValue


def make_knight(x, y):
    entity_id = core.get_id()

    components = [
        Entity(id=entity_id, entity=entity_id, name="knight"),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
        Faction(entity=entity_id, faction=Faction.Options.PEASANT),
        Corpse(entity=entity_id),
        StationaryAttackActor(entity=entity_id, root_x=x, root_y=y),
        CostMapper(entity=entity_id, mapper_type=CostMapperType.NORMAL),
        Appearance(
            entity=entity_id,
            symbol="K",
            color=palettes.STONE,
            bg_color=palettes.BACKGROUND,
        ),
        Attributes(entity=entity_id, hp=10, max_hp=10),
        StandardAttack(entity=entity_id, damage=3),
        Material(entity=entity_id, blocks=False, blocks_sight=False),
        PathfinderCost(entity=entity_id, cost=40),
        Sellable(entity=entity_id, value=0),
        TargetEvaluator(
            entity=entity_id,
            evaluator_type=TargetEvaluatorType.ALLY,
        ),
        TaxValue(entity=entity_id, value=TaxValue.KNIGHT),
    ]

    return entity_id, components
