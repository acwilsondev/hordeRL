#!/usr/bin/env python3

import argparse
import cProfile
import logging
import os

from engine.game_scene_controller import GameSceneController
from scenes.start_menu import get_start_menu


def main():
    game = GameSceneController("Oh No! It's THE HORDE!")
    game.push_scene(get_start_menu())
    game.start()
16|

17|def cli():
18|    parser = argparse.ArgumentParser(description="Oh No! It's THE HORDE!")
19|    parser.add_argument("--prof", action="store_true", help="profile the game")
20|    parser.add_argument(
21|        "--debug", action="store_true", help="allow a crash when an exception is thrown"
22|    )
23|    parser.add_argument(
24|        "-l",
25|        "--log",
26|        choices=["INFO", "WARNING", "CRITICAL", "ERROR", "DEBUG"],
27|        default="INFO",
28|    )
29|    parser.add_argument(
30|        "-t",
31|        "--terminal_log",
32|        action="store_true",
33|        help="log events to terminal instead of file",
34|    )
35|    args = parser.parse_args()
36|
37|    if not args.terminal_log:
38|        logging.basicConfig(
39|            filename="./.log", filemode="a", format="%(levelname)s\t%(message)s"
40|        )
41|    else:
42|        logging.basicConfig(format="%(levelname)s\t%(message)s")
43|
44|    logging.getLogger().setLevel(args.log)
45|
46|    if args.prof:
47|        pr = cProfile.Profile()
48|        pr.enable()
49|        main()
50|        pr.disable()
51|        pr.dump_stats("prof.txt")
52|    else:
53|        main()
54|
55|
56|if __name__ == "__main__":
57|    cli()
58|
