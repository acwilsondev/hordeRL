from abc import ABC, abstractmethod
from dataclasses import dataclass

from horderl.engine.components.component import Component
from horderl.engine.components.events import Event


@dataclass
class StartGame(Event):
    """
    Event triggered when a new game starts.

    This event is dispatched during game initialization to notify all GameStartListener
    components that they should execute their game start behavior. It's a core part of
    the event system that facilitates decoupled communication between the game
    initialization process and components that need to respond to it.

    The event doesn't carry any data as it simply signals that the game has started,
    leaving specific initialization details to the listener components.

    """

    def listener_type(self):
        """
        Return the type of listener that should be notified of this event.

        This method identifies which listener components should receive
        notifications when this event is dispatched. For the StartGame event,
        this returns the GameStartListener class.

        Returns:
            GameStartListener: The class (not an instance) of the listener
                              components that should be notified of this event.

        """
        return GameStartListener

    def notify(self, scene, listener):
        """
        Notify a listener component of the StartGame event.

        This method is called for each GameStartListener component registered
        in the scene when the StartGame event is dispatched. It triggers the
        on_game_start method on the listener, passing the current scene as
        an argument.

        Args:
            scene (GameScene): The current game scene containing the game state.
            listener (GameStartListener): The listener component to notify.

        """
        listener.on_game_start(scene)


class GameStartListener(Component, ABC):
    """
    Abstract base class for components that respond to game start events.

    GameStartListener defines the interface for components that need to perform specific
    actions when a new game starts. This follows the observer pattern, where listeners
    wait for specific events and execute custom logic when those events occur.

    By inheriting from this class and implementing the on_game_start method, components
    can register themselves to be notified when a StartGame event is dispatched without
    having direct dependencies on the event source.

    Implementations should be registered with the component manager to receive
    notifications. The event system will automatically discover all components that
    inherit from this class and notify them when a StartGame event occurs.

    """

    @abstractmethod
    def on_game_start(self, scene):
        """
        Handle the game start event with component-specific behavior.

        This method is called when a StartGame event is dispatched.
        Each concrete implementation must override this method to define
        its specific initialization behavior.

        Args:
            scene: The active game scene containing the game state and
                  component manager.

        Raises:
            NotImplementedError: If the subclass does not implement this method.

        """
        raise NotImplementedError()
