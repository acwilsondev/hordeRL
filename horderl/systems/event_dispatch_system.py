"""
System for dispatching event components to their listeners.
"""

from engine.components.events import Event, dispatch_event


def run(scene) -> None:
    """
    Dispatch all events currently queued in the component manager.

    Args:
        scene: Scene providing the component manager used for dispatch.

    Side Effects:
        - Notifies event listeners.
        - Removes dispatched event components from the component manager.

    """
    for event in list(scene.cm.get(Event)):
        dispatch_event(scene, event)
