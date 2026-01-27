from engine.components import EnergyActor

from ..components.brains.brain import Brain
from .utilities import is_energy_ready


def run(scene):
    player_actor = scene.cm.get_one(Brain, entity=scene.player)
    if player_actor and is_energy_ready(player_actor):
        return
    else:
        actors = scene.cm.get(EnergyActor)
        for actor in actors:
            if actor.is_recharging:
                actor.current_turn += 1
                actor.energy = actor.current_turn - actor.next_turn_to_act
