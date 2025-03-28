from horderl.components import Coordinates
from horderl.components.events.attack_started_events import AttackStartListener
from horderl.components.events.start_game_events import GameStartListener
from horderl.components.tags.town_center_flag import TownCenterFlag


class MovePlayerToTownCenter(GameStartListener, AttackStartListener):
    def on_game_start(self, scene):
        self.move_player(scene)

    def on_season_reset(self, scene):
        self.move_player(scene)

    def on_attack_start(self, scene):
        self.move_player(scene)

    def move_player(self, scene):
        self._log_info(f"moving player to town center")
        flag = scene.cm.get(TownCenterFlag)[0]
        coord = scene.cm.get_one(Coordinates, entity=flag.entity)
        player = scene.cm.get_one(Coordinates, entity=scene.player)
        player.x = coord.x
        player.y = coord.y
