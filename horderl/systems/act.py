from engine.components import Actor

from .attack_action_system import run as run_attack_actions
from .eat_action_system import run as run_eat_actions
from .tunnel_to_point_system import run as run_tunnel_actions


def run(scene) -> None:
    run_attack_actions(scene)
    run_eat_actions(scene)
    run_tunnel_actions(scene)
    for actor in get_actors(scene):
        actor.act(scene)


def get_actors(scene):
    return [
        actor
        for actor in scene.cm.get(Actor)
        if actor.can_act()
        and callable(getattr(actor, "act", None))
    ]
