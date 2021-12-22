import random

import settings
from components import Entity, Appearance, Coordinates
from components.delete_listeners.deleter import Deleter
from components.player_controllers.player_dead_actor import PlayerDeadActor
from components.tags.corpse_tag import CorpseTag
from engine import palettes, core
from engine.constants import PRIORITY_LOW


def make_corpse(name, x, y, symbol='%', color=palettes.BLOOD, bg_color=palettes.BACKGROUND):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name=name),
            Appearance(entity=entity_id, symbol=symbol, color=color, bg_color=bg_color),
            CorpseTag(entity=entity_id),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
            Deleter(entity=entity_id, next_update=core.time_ms() + random.randint(1000, 15000))
        ]
    )


def make_blood_pool(x, y, color):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name=f'blood pool'),
            Appearance(entity=entity_id, symbol='.', color=color, bg_color=palettes.BACKGROUND),
            CorpseTag(entity=entity_id),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
            Deleter(entity=entity_id, next_update=core.time_ms() + random.randint(1000, 15000))
        ]
    )


def make_blood_splatter(count, x, y, color):
    pools = []
    for _ in range(count):
        x2 = x + int(random.triangular(-count, 0, count))
        y2 = y + int(random.triangular(-count, 0, count))

        if 0 < x2 < settings.MAP_WIDTH and 0 < y2 < settings.MAP_HEIGHT:
            pools += make_blood_pool(x2, y2, color)[1]
    return pools


def make_player_corpse(x, y):
    """Create a corpse with some remaining agency."""
    entity_id = core.get_id()

    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name='player corpse'),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
            Appearance(entity=entity_id, symbol='%', color=palettes.BLOOD, bg_color=palettes.BACKGROUND),
            PlayerDeadActor(entity=entity_id),
        ]
    )
