#!/usr/bin/env python3

import argparse
import cProfile
import logging
import os

from horderl.engine.game_scene_controller import GameSceneController
from horderl.engine.logging import configure_logging
from horderl.scenes.start_menu import get_start_menu


def main():
    game = GameSceneController("Oh No! It's THE HORDE!")
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

    # Convert string log level to logging constant
    log_level = getattr(logging, args.log)
    
    # Configure logging based on arguments
    if args.terminal_log:
        # Terminal-only logging (disable file logging)
        configure_logging(
            environment="development",
            console_level=log_level,
            log_dir=os.path.dirname(os.path.abspath(__file__)),
            log_file=None
        )
    else:
        # Both terminal and file logging
        configure_logging(
            environment="development",
            console_level=log_level,
            file_level=log_level,
            log_dir=os.path.dirname(os.path.abspath(__file__)),
            log_file=".log"
        )

    if args.prof:
        pr = cProfile.Profile()
        pr.enable()
        main()
        pr.disable()
        pr.dump_stats("prof.txt")
    else:
        main()


if __name__ == "__main__":
    cli()
