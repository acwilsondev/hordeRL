from dataclasses import dataclass

from horderl.components.events.die_events import DeathListener
from horderl.components.house_structure import HouseStructure
from horderl.engine import constants


@dataclass
class ScheduleRebuild(DeathListener):
    """
    When this wall dies, set a delayed trigger to attempt to rebuild at the season
    reset.
    """

    root: int = constants.INVALID

    def on_die(self, scene):
        self._log_info("scheduled rebuild")
        house_structure = scene.cm.get_one(HouseStructure, entity=self.root)
        if house_structure:
            house_structure.is_destroyed = True
