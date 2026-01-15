from dataclasses import dataclass

from engine.components import EnergyActor

from ..components.events.hole_dug_events import HoleDugListener
from ..systems.flood_holes_system import run as run_flood_holes


@dataclass
class FloodHolesController(EnergyActor, HoleDugListener):
    """
    Coordinate hole flooding by delegating flood-fill logic to the system layer.

    This component holds the state required to throttle flood fills over time,
    while the actual fill logic lives in the flood holes system.
    """

    flood_tick: int = 0
    is_recharging: bool = False
    energy_cost: int = EnergyActor.HALF_HOUR

    def on_hole_dug(self, scene) -> None:
        """
        Enable flooding when a new hole is dug.

        Args:
            scene: The active game scene that owns the component manager.

        Returns:
            None.

        Side Effects:
            Sets the controller to begin recharging energy so flood fills can occur.
        """
        self._log_debug("beginning to fill nearby holes")
        self.is_recharging = True

    def act(self, scene) -> None:
        """
        Trigger a flood-fill step.

        Args:
            scene: The active game scene that owns the component manager.

        Returns:
            None.

        Side Effects:
            Delegates flood-fill logic to the flood holes system, which may create
            water entities, delete holes, and adjust energy/cooldowns.
        """
        run_flood_holes(scene, self)
