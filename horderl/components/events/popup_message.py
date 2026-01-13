from dataclasses import dataclass

from horderl.components.animation_controllers.real_time_actor import RealTimeActor


@dataclass
class PopupMessage(RealTimeActor):
    timer_delay: int = RealTimeActor.REAL_TIME
    message: str = ""

    def act(self, scene):
        if self.next_update:
            scene.popup_message(self.message)
            scene.cm.delete_component(self)
