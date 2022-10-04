#!/usr/bin/env python3
from Game import Game
from config import Config
import curses


def main(stdscr, config):
    game = Game(stdscr, config)
    game.play()
    return 0


if __name__ == '__main__':
    import sys
    config = Config
    if len(sys.argv) > 1:
        arg = sys.argv[1].rstrip().lower()
        if arg == "--daily":
            config.setdaily()
        elif len(arg) == config.WORDLEN and arg in config.VALIDWORDS:
            Config.SOLUTION = arg
        else:
            print(f"Word not in list")
            sys.exit(2)
    try:
        sys.exit(curses.wrapper(main, config))
    except KeyboardInterrupt:
        sys.exit(0)
    except OverflowError:
        print("Couldn't start display.")
        print("Window needs to be at least 27x16")
        sys.exit(1)
