from engine import core

from ...content.farmsteads.houses import place_farmstead


def place_peasants(scene):
    """Place farmsteads in the world."""
    logger = core.get_logger(__name__)
    logger.info(f"placing farmsteads...")
    for _ in range(3):
        place_farmstead(scene)
    logger.info(f"farmsteads placed.")
