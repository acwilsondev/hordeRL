#!/usr/bin/env python3

import argparse
import cProfile
import logging
import os

from horderl.config import get_relative_path, load_config
from horderl.engine.game_scene_controller import GameSceneController
from horderl.engine.logging import configure_logging
from horderl.scenes.start_menu import get_start_menu


def main(config):
    game = GameSceneController("Oh No! It's THE HORDE!", config)
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
        "-l",
        "--log",
        choices=["INFO", "WARNING", "CRITICAL", "ERROR", "DEBUG"],
        default="INFO",
    )
    parser.add_argument(
        "-t",
        "--terminal_log",
        action="store_true",
        help="log events to terminal instead of file",
    )
    args = parser.parse_args()
    config = load_config(
        args.options_path or get_relative_path("options.yaml"),
        overrides={
            "character_name": args.character_name,
            "world_seed": args.world_seed,
            "torch_radius": args.torch_radius,
            "grass_density": args.grass_density,
            "autosave_enabled": args.autosave_enabled,
            "music_enabled": args.music_enabled,
        },
    )

    # Convert string log level to logging constant
    log_level = getattr(logging, args.log)

    # Configure logging based on arguments
    if args.terminal_log:
        # Terminal-only logging (disable file logging)
        configure_logging(
            environment="development",
            console_level=log_level,
            log_dir=os.path.dirname(os.path.abspath(__file__)),
            log_file=None,
        )
    else:
        # Both terminal and file logging
        configure_logging(
            environment="development",
            console_level=log_level,
            file_level=log_level,
            log_dir=os.path.dirname(os.path.abspath(__file__)),
            log_file=".log",
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
