from dataclasses import dataclass

from horderl.components.events.step_event import EnterListener


@dataclass
class DieOnEnter(EnterListener):
    """
    Data-only configuration for dying when stepped on.
    """
