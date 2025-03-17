from collections import OrderedDict


def get_start_menu():
    from horderl.scenes.defend_scene import DefendScene
    from horderl.scenes.load_game_scene import LoadMenuScene
    from horderl.scenes.navigation_menu_scene import NavigationMenuScene
    from horderl.scenes.quit_scene import QuitScene

    option_map = OrderedDict()
    option_map["New Game"] = DefendScene()
    option_map["Load Game"] = LoadMenuScene()
    option_map["Quit"] = QuitScene()
    return NavigationMenuScene(
        title="Oh No! It's THE HORDE!",
        option_scene_map=option_map,
    )
