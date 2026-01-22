from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class StartGame(Component):
    """
    Event triggered when a new game starts.

    This event is dispatched during game initialization to notify all GameStartListener
    components that they should execute their game start behavior. It's a core part of
    the event system that facilitates decoupled communication between the game
    initialization process and components that need to respond to it.

    The event doesn't carry any data as it simply signals that the game has started,
    leaving specific initialization details to the listener components.

    """


@dataclass
class GameStartListener(Component):
    """
    Marker component for entities that respond to game start events.

    Components inheriting from this class are discovered by the event system and routed
    to start-game handler functions defined in the systems layer.
    """
