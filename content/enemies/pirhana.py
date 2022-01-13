import random

from components import Coordinates, Appearance, Attributes
from engine.components.energy_actor import EnergyActor
from components.brains.default_active_actor import DefaultActiveActor
from components.attacks.standard_attack import StandardAttack
from components.death_listeners.drop_gold import DropGold
from components.death_listeners.npc_corpse import Corpse
from components.faction import Faction
from components.material import Material
from components.movement.move import Move
from components.pathfinding.normal_cost_mapper import NormalCostMapper
from components.pathfinding.target_evaluation.high_crop_target_evaluator import HighCropTargetEvaluator
from components.movement.drain_on_water_step import DrainOnStepOnWater
from components.stomach import Stomach
from components.tags.hordeling_tag import HordelingTag
from components.pathfinder_cost import PathfinderCost
from engine import core, palettes
from engine.components.entity import Entity
from engine.constants import PRIORITY_MEDIUM


def make_pirhana(x, y):
    entity_id = core.get_id()

    components = [
        Entity(id=entity_id, entity=entity_id, name='voracious hordeling'),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
        Faction(entity=entity_id, faction=Faction.Options.MONSTER),
        Corpse(entity=entity_id),
        DefaultActiveActor(entity=entity_id),
        NormalCostMapper(entity=entity_id),
        Appearance(entity=entity_id, symbol='v', color=palettes.HORDELING, bg_color=palettes.BACKGROUND),
        Attributes(entity=entity_id, hp=1, max_hp=1),
        StandardAttack(entity=entity_id, damage=1),
        Material(entity=entity_id, blocks=True, blocks_sight=False),
        HordelingTag(entity=entity_id),
        Move(entity=entity_id, energy_cost=EnergyActor.FAST),
        PathfinderCost(entity=entity_id, cost=5),
        Stomach(entity=entity_id),
        HighCropTargetEvaluator(entity=entity_id),
        DrainOnStepOnWater(entity=entity_id)
    ]

    if random.randint(1, 10) == 10:
        components.append(DropGold(entity=entity_id))

    return (
        entity_id,
        components
    )
