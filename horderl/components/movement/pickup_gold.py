from dataclasses import dataclass

from ..events.step_event import StepListener


@dataclass
class PickupGoldOnStep(StepListener):
    """
    Data-only configuration for collecting gold when stepping on it.
    """
