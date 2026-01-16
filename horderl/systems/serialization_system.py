"""System for processing save and load requests."""

from engine import GameScene, core
from engine.logging import get_logger
from horderl import palettes
from horderl.components.events.start_game_events import StartGame
from horderl.components.serialization.load_game import LoadGame
from horderl.components.serialization.save_game import SaveGame
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.i18n import t


def run(scene: GameScene) -> None:
    """
    Process pending load and save requests for the current scene.

    Args:
        scene: Active game scene containing a component manager and IO hooks.

    Side Effects:
        - Loads or saves game state from disk.
        - Emits user-facing messages on completion.
        - Deletes processed request components from the component manager.
    """
    for load_request in list(scene.cm.get(LoadGame)):
        load_game(scene, load_request)

    for save_request in list(scene.cm.get(SaveGame)):
        save_game(scene, save_request)


def load_game(scene: GameScene, request: LoadGame) -> None:
    """
    Load and deserialize game state from the file referenced by the request.

    Args:
        scene: Active game scene containing component manager and IO hooks.
        request: LoadGame configuration describing the file to load.

    Returns:
        None

    Side Effects:
        - Replaces component manager state with serialized data.
        - Logs load performance metrics.
        - Adds game start events captured before the load.
        - Posts a message to the player.
    """
    logger = get_logger(__name__)
    pending_start_events = list(scene.cm.get(StartGame))

    # we don't want this object to get caught in the load operation
    scene.cm.delete_component(request)

    start = core.time_ms()
    logger.info("attempting to read game")
    data = scene.load_game(request.file_name)
    scene.cm.from_data(data)
    end = core.time_ms()
    logger.info("loaded %s objects in %sms", len(data), end - start)

    for event in pending_start_events:
        scene.cm.add(StartGame(entity=event.entity))

    scene.message(t("message.game_loaded"), color=palettes.LIGHT_WATER)


def save_game(scene: GameScene, request: SaveGame) -> None:
    """
    Save the current game state to disk using the request configuration.

    Args:
        scene: Active game scene containing component manager and IO hooks.
        request: SaveGame configuration describing extra data to store.

    Returns:
        None

    Side Effects:
        - Serializes component manager state to disk.
        - Logs save progress.
        - Posts a message to the player.
    """
    logger = get_logger(__name__)

    # remove request before serializing to avoid storing it in the save payload
    scene.cm.delete_component(request)

    logger.info("attempting to save game")
    params = scene.cm.get_one(WorldParameters, entity=core.get_id("world"))
    scene.save_game(
        scene.cm.get_serial_form(),
        f"./{params.get_file_name()}.world",
        request.extra,
    )
    logger.info("save complete")
    scene.message(t("message.game_saved"), color=palettes.LIGHT_WATER)
