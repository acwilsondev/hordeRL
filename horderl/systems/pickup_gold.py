from engine.components import Coordinates
from engine.logging import get_logger

from ..components.pickup_gold import GoldPickup
from ..constants import PLAYER_ID


def run(scene):
    """
    Process all gold pickup events in the scene.

    Args:
        scene: Active scene containing component manager.

    Side Effects:
        - Processes each GoldPickup event and applies rewards.
    """
    for event in scene.cm.get(GoldPickup):
        pickup_gold(scene, event)


def pickup_gold(scene, event):
    """
    Apply a gold pickup event if the player occupies the same tile.

    Args:
        scene: Active scene containing component manager and player state.
        event (GoldPickup): Gold pickup event component.

    Side Effects:
        - Deletes the gold entity when collected.
        - Increments scene.gold for the player.
    """
    logger = get_logger(__name__)
    logger.debug(
        "Checking gold pickup",
        extra={"entity": event.entity, "amount": event.amount},
    )
    # if the player is standing on this the gold nugget, delete the gold nugget
    # and add 10 to their gold.
    coords = scene.cm.get_one(Coordinates, entity=event.entity)
    player_coords = scene.cm.get_one(Coordinates, entity=PLAYER_ID)

    if not player_coords:
        # player might be dead
        return

    if coords.x == player_coords.x and coords.y == player_coords.y:
        scene.cm.delete(event.entity)
        scene.gold += event.amount
