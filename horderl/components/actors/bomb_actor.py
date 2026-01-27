from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class BombActor(EnergyActor):
    """
    Actor component that counts down to an explosion.

    Explosion logic is handled by the actor system.
    """

    turns: int = 3
    next_turn_to_act: int = EnergyActor.HOURLY
