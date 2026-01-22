from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class ShowHelpDialogue(EnergyActor):
    """Request that the help dialogue be shown."""
