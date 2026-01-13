from engine.game_scene_controller import GameSceneController
from engine.ui.gui import Gui
from engine.ui.gui_adapter import GuiAdapter
from horderl import palettes
from horderl.gui.popup_message import PopupMessage
from horderl.i18n import t
from horderl.resources.audio import TRACKS
from horderl.scenes.start_menu import get_start_menu


def build_game_controller(config) -> GameSceneController:
    palettes.apply_config(config)
    gui = Gui(
        config.screen_width,
        config.screen_height,
        title=t("game.title"),
        font_path=config.font,
    )
    ui_context = GuiAdapter(gui, popup_factory=PopupMessage)
    game = GameSceneController(t("game.title"), config, gui, ui_context, TRACKS)
    game.push_scene(get_start_menu())
    return game


def start_game(config) -> GameSceneController:
    game = build_game_controller(config)
    game.start()
    return game
