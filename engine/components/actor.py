from typing import Any, Optional

from engine.components.component import Component


class Actor(Component):
    """
    Provides control and other 'mind' information.
    """

    # action management
    intention: Optional[Any] = None
    intention_target: Optional[int] = None

    def can_act(self) -> bool:
        """
        Return whether the actor is currently able to act.
        """
        return False
