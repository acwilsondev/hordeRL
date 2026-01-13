#!/usr/bin/env python3

import argparse
import cProfile
import logging
import os

from engine.game_scene_controller import GameSceneController
from engine.logging import configure_logging
from engine.ui.gui import Gui
from engine.ui.gui_adapter import GuiAdapter
from horderl import palettes
from horderl.config import get_relative_path, load_config
from horderl.gui.popup_message import PopupMessage
from horderl.i18n import load_locale, t
from horderl.resources.audio import TRACKS
from horderl.scenes.start_menu import get_start_menu


def main(config):
    palettes.apply_config(config)
    gui = Gui(
        config.screen_width,
        config.screen_height,
        title=t("game.title"),
        font_path=config.font,
    )
    ui_context = GuiAdapter(gui, popup_factory=PopupMessage)
    game = GameSceneController(
        t("game.title"), config, gui, ui_context, TRACKS
    )
    game.push_scene(get_start_menu())
    game.start()


def cli():
    parser = argparse.ArgumentParser(description="Oh No! It's THE HORDE!")
    parser.add_argument("--prof", action="store_true", help="profile the game")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="allow a crash when an exception is thrown",
    )
    parser.add_argument(
        "--options-path",
        default=None,
        help="path to options.yaml (defaults to the packaged options.yaml)",
    )
    parser.add_argument(
        "--character-name",
        dest="character_name",
        default=None,
        help="override the player character name",
    )
    parser.add_argument(
        "--locale",
        dest="locale",
        default=None,
        help="override the locale code for translations",
    )
    parser.add_argument(
        "--seed",
        dest="world_seed",
        default=None,
        help="override the world seed",
    )
    parser.add_argument(
        "--torch-radius",
        type=int,
        default=None,
        help="override the torch radius",
    )
    parser.add_argument(
        "--grass-density",
        type=float,
        default=None,
        help="override the grass density",
    )
    parser.add_argument(
        "--autosave",
        dest="autosave_enabled",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="enable or disable autosave",
    )
    parser.add_argument(
        "--music",
        dest="music_enabled",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="enable or disable music",
    )
    parser.add_argument(
        "--color-palette",
        dest="color_palette",
        default=None,
        help="override the color palette name or path",
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="log_level",
        choices=["INFO", "WARNING", "CRITICAL", "ERROR", "DEBUG"],
        default=None,
    )
    parser.add_argument(
        "-t",
        "--terminal_log",
        action="store_true",
        help="log events to terminal instead of file",
    )
    parser.add_argument(
        "--log-environment",
        dest="log_environment",
        choices=["development", "test", "production"],
        default=None,
        help="override the logging environment",
    )
    parser.add_argument(
        "--log-dir",
        dest="log_dir",
        default=None,
        help="override the directory for log files",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        default=None,
        help="override the log file name (set empty to disable file logging)",
    )
    parser.add_argument(
        "--log-console",
        dest="log_console_enabled",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="enable or disable console logging",
    )
    args = parser.parse_args()
    config = load_config(
        args.options_path or get_relative_path("options.yaml"),
        overrides={
            "character_name": args.character_name,
            "locale": args.locale,
            "world_seed": args.world_seed,
            "torch_radius": args.torch_radius,
            "grass_density": args.grass_density,
            "autosave_enabled": args.autosave_enabled,
            "music_enabled": args.music_enabled,
            "color_palette": args.color_palette,
            "log_environment": args.log_environment,
            "log_level": args.log_level,
            "log_dir": args.log_dir,
            "log_file": args.log_file if args.log_file != "" else None,
            "log_console_enabled": args.log_console_enabled,
        },
    )
    load_locale(config.locale)

    if args.terminal_log:
        config.log_console_enabled = True
        config.log_file = None

    # Convert string log level to logging constant
    log_level = getattr(logging, config.log_level)

    # Configure logging based on arguments
    configure_logging(
        environment=config.log_environment,
        console_level=log_level,
        file_level=log_level,
        log_dir=config.log_dir or os.path.dirname(os.path.abspath(__file__)),
        log_file=config.log_file,
        console_enabled=config.log_console_enabled,
    )

    if args.prof:
        pr = cProfile.Profile()
        pr.enable()
        main(config)
        pr.disable()
        pr.dump_stats("prof.txt")
    else:
        main(config)


if __name__ == "__main__":
    cli()
