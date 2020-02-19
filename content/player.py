from components import Entity, Appearance, Senses, Brain, Attributes
from components.attack import Attack
from components.enums import ControlMode
from components.target_value import PLAYER, TargetValue
from engine import colors, PLAYER_ID


def make_player(zone_id):
    entity_id = PLAYER_ID

    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name='player', zone=zone_id),
            Appearance(entity=entity_id, symbol='@', color=colors.white),
            Senses(entity=entity_id, sight_radius=10),
            Brain(entity=entity_id, control_mode=ControlMode.PLAYER, take_turn=True),
            Attributes(entity=entity_id, hp=60, max_hp=60),
            Attack(entity=entity_id, damage='1d10'),
            TargetValue(entity=entity_id, value=PLAYER)
        ]
    )
