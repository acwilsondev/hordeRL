from dataclasses import dataclass

from engine.components import Actor
from horderl.components.events.delete_event import DeleteListener
from horderl.components.relationships.owner import Owner


@dataclass
class ResetOwnerAnimation(DeleteListener):
    def on_delete(self, scene):
        owner = scene.cm.get_one(Owner, entity=self.entity)

        # todo unhardcode this
        peasant = scene.cm.get_one(Actor, entity=owner.owner)
        self._log_debug(f"triggered, owner={owner.owner}")

        peasant.can_animate = True
