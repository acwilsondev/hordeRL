from collections import OrderedDict

from horderl.i18n import t


def get_start_menu():
    from horderl.scenes.defend_scene import DefendScene
    from horderl.scenes.load_game_scene import LoadMenuScene
    from horderl.scenes.navigation_menu_scene import NavigationMenuScene
    from horderl.scenes.quit_scene import QuitScene

    option_map = OrderedDict()
    option_map[t("menu.new_game")] = DefendScene()
    option_map[t("menu.load_game")] = LoadMenuScene()
    option_map[t("menu.quit")] = QuitScene()
    return NavigationMenuScene(
        title=t("game.title"),
        option_scene_map=option_map,
    )
