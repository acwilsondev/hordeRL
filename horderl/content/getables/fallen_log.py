from horderl.components import Appearance, Coordinates
from horderl.components.material import Material
from horderl.components.pickup_gold import GoldPickup
from horderl.engine import core, palettes
from horderl.engine.components.entity import Entity
from horderl.engine.constants import PRIORITY_LOW

description = (
    "A log has fallen here. This will fetch a fair price on the market."
)


def make_fallen_log(x, y):
    entity_id = core.get_id()

    return (
        entity_id,
        [
            Entity(
                id=entity_id,
                entity=entity_id,
                name="fallen log",
                description=description,
            ),
            Appearance(
                entity=entity_id,
                symbol="=",
                color=palettes.WOOD,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
            GoldPickup(entity=entity_id, amount=5),
            Material(entity=entity_id, blocks=False, blocks_sight=False),
        ],
    )
