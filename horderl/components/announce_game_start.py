from ..components.events.start_game_events import GameStartListener
from ..i18n import t


class AnnounceGameStart(GameStartListener):
    def on_game_start(self, scene):
        scene.message(
            t("message.start.protect")
        )
        scene.message(
            t("message.start.horde")
        )
        scene.message(t("message.start.help"))
        scene.cm.delete_component(self)
