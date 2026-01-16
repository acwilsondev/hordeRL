from .ability_system import run as run_ability_system
from .actor_system import run as run_actor_system
from .attack_action_system import run as run_attack_actions
from .brain_system import run as run_brain_system
from .debug_menu import run as run_debug_menu
from .eat_action_system import run as run_eat_actions
from .tunnel_to_point_system import run as run_tunnel_actions


def run(scene) -> None:
    run_attack_actions(scene)
    run_ability_system(scene)
    run_eat_actions(scene)
    run_tunnel_actions(scene)
    run_debug_menu(scene)
    run_brain_system(scene)
    run_actor_system(scene)
