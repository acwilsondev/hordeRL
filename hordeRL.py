#!/usr/bin/env python3

import argparse
import cProfile
import logging

from horderl.engine.game_scene_controller import GameSceneController
from horderl.scenes.start_menu import get_start_menu


def main():
    game = GameSceneController("Oh No! It's THE HORDE!")
    game.push_scene(get_start_menu())
    game.start()


def cli():
    parser = argparse.ArgumentParser(description="Oh No! It's THE HORDE!")
    parser.add_argument("--prof", action="store_true", help="profile the game")
    parser.add_argument(
        "--debug", action="store_true", help="allow a crash when an exception is thrown"
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

    if not args.terminal_log:
        logging.basicConfig(
            filename="./.log", filemode="a", format="%(levelname)s\t%(message)s"
        )
    else:
        logging.basicConfig(format="%(levelname)s\t%(message)s")

    logging.getLogger().setLevel(args.log)

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
