from engine.components import EnergyActor

from ..components.brains.brain import Brain


def run(scene):
    player_actor = scene.cm.get_one(Brain, entity=scene.player)
    if (
        player_actor
        and player_actor.current_turn >= player_actor.next_turn_to_act
    ):
        return
    else:
        actors = scene.cm.get(EnergyActor)
        for actor in actors:
            if actor.is_recharging:
                actor.current_turn += 1
                actor.energy = actor.current_turn - actor.next_turn_to_act
