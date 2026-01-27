from engine import core
from horderl.components.world_turns import WorldTurns

from ..components.brains.brain import Brain


def run(scene):
    world_turns = scene.cm.get_one(WorldTurns, entity=core.get_id("world"))
    if not world_turns:
        return
    player_actor = scene.cm.get_one(Brain, entity=scene.player)
    if player_actor and player_actor.can_act(world_turns):
        return
    else:
        world_turns.current_turn += 1
