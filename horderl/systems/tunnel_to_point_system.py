from engine.components import Coordinates
from horderl.components.actions.tunnel_to_point import TunnelToPoint
from horderl.content.terrain.hole import make_hole
from horderl.systems.utilities import get_current_turn


def run(scene) -> None:
    """
    Resolve queued tunnel actions.

    Args:
        scene: Active game scene.

    Side effects:
        - Moves the tunneling entity.
        - Spawns holes.
        - Deletes TunnelToPoint components.
    """
    current_turn = get_current_turn(scene)
    for action in scene.cm.get(TunnelToPoint):
        if action.can_act(current_turn):
            execute(scene, action)


def execute(scene, action: TunnelToPoint) -> None:
    """
    Execute a tunnel-to-point action.

    Args:
        scene: Active game scene.
        action: The tunnel action data component.
    """
    action._log_info(f"tunnelling to point {action.point}")
    coords = scene.cm.get_one(Coordinates, entity=action.entity)
    coords.x = action.point[0]
    coords.y = action.point[1]
    scene.cm.add(*make_hole(coords.x, coords.y)[1])
    scene.cm.delete_component(action)
