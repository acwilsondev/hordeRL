from abc import abstractmethod
from dataclasses import dataclass

from engine import GameScene
from engine.components import EnergyActor
from engine.core import log_debug


@dataclass
class Event(EnergyActor):
    """
    Define an event that notifies listeners.
    """

    energy_cost: int = EnergyActor.INSTANT

    @log_debug(__name__)
    def act(self, scene: GameScene) -> None:
        """
        Dispatch the event to its listeners.

        Args:
            scene (GameScene): Active scene providing access to the component manager.

        Side Effects:
            - Notifies all matching listeners.
            - Deletes the event component from the component manager.
            - Executes before/after hooks on the event.

        """
        dispatch_event(scene, self)

    @abstractmethod
    def listener_type(self):
        """
        Return the type of listener to notify.
        """
        raise NotImplementedError("Must subclass Event")

    @abstractmethod
    def notify(self, scene: GameScene, listener) -> None:
        """
        Notify a listener of the event.
        """
        raise NotImplementedError("Must subclass Event")

    def _before_notify(self, scene: GameScene) -> None:
        """
        Define actions to take before listeners have been notified.
        """

    def _after_notify(self, scene: GameScene) -> None:
        """
        Define actions to take after listeners have been notified but before deleting
        the event.
        """

    def _after_remove(self, scene: GameScene) -> None:
        pass


def dispatch_event(scene: GameScene, event: Event) -> None:
    """
    Dispatch an event to matching listeners and remove it from the scene.

    Args:
        scene (GameScene): Scene containing the component manager used for dispatch.
        event (Event): Event instance to dispatch.

    Side Effects:
        - Logs the dispatch for the event instance.
        - Notifies all listeners returned by event.listener_type().
        - Deletes the event component from the component manager.
        - Runs before/after notification hooks on the event.

    """
    event._log_info("event")
    event._before_notify(scene)
    listeners = scene.cm.get(event.listener_type())
    for listener in listeners:
        event.notify(scene, listener)
    event._after_notify(scene)
    scene.cm.delete_component(event)
    event._after_remove(scene)
