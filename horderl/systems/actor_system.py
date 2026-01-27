"""System routines for non-brain actor components."""

import random
from typing import List, Tuple

from engine import core
from engine.components import Coordinates, EnergyActor
from engine.logging import get_logger
from engine.utilities import get_3_by_3_square
from horderl.components import Attributes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.actors.bomb_actor import BombActor
from horderl.components.actors.calendar_actor import Calendar
from horderl.components.actors.hordeling_spawner import HordelingSpawner
from horderl.components.events.attack_started_events import AttackStarted
from horderl.components.events.die_events import Die
from horderl.components.events.new_day_event import DayBegan
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.tags.tag import Tag, TagType
from horderl.components.world_beauty import WorldBeauty
from horderl.content.explosion import make_explosion
from horderl.content.spawners.hordeling_spawner_spawner import (
    hordeling_spawner,
)
from horderl.content.states import character_animation
from horderl.i18n import t
from horderl.systems.utilities import (
    can_actor_act,
    get_current_turn,
    pass_actor_turn,
)

ACTOR_HANDLERS = (
    (BombActor, "run_bomb_actor"),
    (Calendar, "run_calendar"),
    (HordelingSpawner, "run_hordeling_spawner"),
)


def run(scene) -> None:
    """
    Run all active non-brain actor components for the current scene.

    Args:
        scene: Active scene containing component manager and config.

    Side Effects:
        - Advances timers, spawns entities, or resolves explosions.
    """
    for actor in get_active_actors(scene):
        run_actor(scene, actor)


def get_active_actors(scene) -> List[EnergyActor]:
    """
    Collect non-brain actors that are ready to act.

    Args:
        scene: Active scene containing component manager.

    Returns:
        List[EnergyActor]: Active actor components that can act.
    """
    from horderl.components.brains.brain import Brain

    current_turn = get_current_turn(scene)
    return [
        actor
        for actor in scene.cm.get(EnergyActor)
        if not isinstance(actor, Brain) and can_actor_act(actor, current_turn)
    ]


def run_actor(scene, actor: EnergyActor) -> None:
    """
    Dispatch an actor component to its behavior handler.

    Args:
        scene: Active scene containing component manager and config.
        actor: Actor component to execute.

    Side Effects:
        - Triggers actor-specific logic depending on the component type.
    """
    for actor_type, handler_name in ACTOR_HANDLERS:
        if isinstance(actor, actor_type):
            handler = globals()[handler_name]
            handler(scene, actor)
            return
    get_logger(__name__).warning(
        "No actor handler registered",
        extra={"entity": actor.entity, "actor_type": type(actor).__name__},
    )


def run_bomb_actor(scene, actor: BombActor) -> None:
    """
    Execute the countdown and explosion behavior for a bomb.

    Args:
        scene: Active scene containing component manager and config.
        actor: BombActor component for the entity.

    Side Effects:
        - Adds attack actions, explosions, and die events.
        - Consumes time via pass_actor_turn().
    """
    coords = scene.cm.get_one(Coordinates, entity=actor.entity)
    current_turn = get_current_turn(scene)
    if actor.turns <= 0:
        _explode(scene, actor)
        pass_actor_turn(actor, current_turn)
        return
    scene.cm.add(*character_animation(coords.x, coords.y, f"{actor.turns}")[1])
    actor.turns -= 1
    pass_actor_turn(actor, current_turn)


def run_calendar(scene, actor: Calendar) -> None:
    """
    Advance the calendar and manage horde phases.

    Args:
        scene: Active scene containing component manager and config.
        actor: Calendar component for the entity.

    Side Effects:
        - Emits day/season events and spawns hordes.
        - Updates calendar status and scheduling.
    """
    if actor.day < 25:
        actor.status = t("status.peacetime")
        _increment_calendar(actor, get_current_turn(scene))
        scene.cm.add(DayBegan(entity=actor.entity, day=actor.day))
    elif actor.day < 30:
        actor.status = t("status.horde_approaching")
        _increment_calendar(actor, get_current_turn(scene))
        scene.cm.add(DayBegan(entity=actor.entity, day=actor.day))
    else:
        if actor.status != t("status.under_attack"):
            _start_attack(scene, actor)
        if not still_under_attack(scene):
            _end_attack(scene, actor)


def run_hordeling_spawner(scene, actor: HordelingSpawner) -> None:
    """
    Spawn hordelings over multiple waves.

    Args:
        scene: Active scene containing component manager and config.
        actor: HordelingSpawner component for the entity.

    Side Effects:
        - Adds enemy components to the scene.
        - Consumes time and deletes the spawner when done.
    """
    spawn_hordeling(scene)
    pass_actor_turn(
        actor,
        get_current_turn(scene),
        random.randint(EnergyActor.QUARTER_HOUR, EnergyActor.HOURLY * 20),
    )

    actor.waves -= 1

    if actor.waves <= 0:
        scene.cm.delete(actor.entity)


def get_timecode(calendar: Calendar) -> str:
    """
    Return a formatted timecode string for a calendar.

    Args:
        calendar: Calendar component to render.

    Returns:
        str: Localized timecode string.
    """
    season = get_season_string(calendar)
    return t(
        "timecode.format",
        season=t(f"season.{season.lower()}"),
        day=calendar.day,
        year=calendar.year,
    )


def get_season_string(calendar: Calendar) -> str:
    """
    Translate the calendar's season number into a label.

    Args:
        calendar: Calendar component to render.

    Returns:
        str: Season name.
    """
    return {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}[calendar.season]


def still_under_attack(scene) -> bool:
    """
    Report whether any hordelings are still present.

    Args:
        scene: Active scene containing component manager.

    Returns:
        bool: True if any hordeling spawners or units remain.
    """
    return (
        scene.cm.get(HordelingSpawner)
        or scene.cm.get(HordelingSpawner)
        or scene.cm.get(
            Tag, query=lambda tag: tag.tag_type == TagType.HORDELING
        )
    )


def spawn_hordeling(scene) -> None:
    """
    Spawn a single hordeling along the map edge.

    Args:
        scene: Active scene containing component manager and config.

    Side Effects:
        - Adds enemy components at the spawn location.
    """
    from horderl.content.enemies.juggernaut import make_juggernaut
    from horderl.content.enemies.juvenile import make_juvenile
    from horderl.content.enemies.pirhana import make_pirhana
    from horderl.content.enemies.sneaker import make_sneaker

    x, y = _get_wall_coords(scene.config)
    roll = random.random()
    if roll > 0.8:
        maker = random.choice([make_sneaker, make_juggernaut, make_pirhana])
        scene.cm.add(*maker(x, y)[1])
    else:
        scene.cm.add(*make_juvenile(x, y)[1])


def _increment_calendar(calendar: Calendar, current_turn: int) -> None:
    """# Updates day, season, year, and consumes time."""
    calendar.day += 1
    if calendar.day > MAX_DAY:
        calendar.season += 1
        calendar.day = 1

    if calendar.season > MAX_SEASON:
        calendar.year += 1
        calendar.season = 1
    pass_actor_turn(calendar, current_turn)


def _start_attack(scene, calendar: Calendar) -> None:
    """# Starts an attack and spawns hordeling spawners."""
    scene.popup_message(t("message.horde_arrival"))
    spirits_wrath = scene.cm.get_one(
        WorldBeauty, entity=core.get_id("world")
    ).spirits_wrath

    scene.cm.add(*hordeling_spawner(waves=calendar.round + spirits_wrath)[1])
    scene.cm.add(AttackStarted(entity=scene.player))
    calendar.is_recharging = False
    calendar.status = t("status.under_attack")


def _end_attack(scene, calendar: Calendar) -> None:
    """# Ends an attack and fires season reset events."""
    calendar.status = t("status.peacetime")
    calendar.round += 1
    calendar.is_recharging = True
    _increment_calendar(calendar, get_current_turn(scene))
    scene.cm.add(DayBegan(entity=calendar.entity))
    scene.cm.add(
        ResetSeason(entity=calendar.entity, season=get_season_string(calendar))
    )


def _explode(scene, actor: BombActor) -> None:
    """# Explosion applies damage and visual effects to nearby tiles."""
    attributes: List[Attributes] = scene.cm.get(Attributes)
    targets = set()
    for attribute in attributes:
        if _is_adjacent(scene, attribute.entity, actor.entity):
            targets.add(attribute.entity)
    for target in list(targets):
        scene.cm.add(
            AttackAction(entity=actor.entity, target=target, damage=3)
        )

    coords = scene.cm.get_one(Coordinates, entity=actor.entity)
    explosion_area = get_3_by_3_square(coords.x, coords.y)
    for explosion in explosion_area:
        scene.cm.add(*make_explosion(explosion[0], explosion[1])[1])

    scene.warn("A bomb exploded!")
    scene.cm.add(Die(entity=actor.entity, killer=actor.entity))


def _is_adjacent(scene, first: int, second: int) -> bool:
    """# Adjacency is measured via coordinate distance."""
    first_coord: Coordinates = scene.cm.get_one(Coordinates, entity=first)
    second_coord: Coordinates = scene.cm.get_one(Coordinates, entity=second)
    return (
        first_coord
        and second_coord
        and first_coord.distance_from(second_coord) < 2
    )


def _get_wall_coords(config) -> Tuple[int, int]:
    """# Returns random coordinate along the map border."""
    return random.choice(
        [
            (_get_random_width_location(config), 0),
            (0, _get_random_height_location(config)),
            (config.map_width - 1, _get_random_height_location(config)),
            (_get_random_width_location(config), config.map_height - 1),
        ]
    )


def _get_random_width_location(config) -> int:
    """# Ensures edge spawns avoid corners."""
    return random.randrange(1, config.map_width - 1)


def _get_random_height_location(config) -> int:
    """# Ensures edge spawns avoid corners."""
    return random.randrange(1, config.map_height - 1)


MAX_HOUR = 23
MAX_DAY = 30
MAX_SEASON = 4
