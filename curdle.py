#!/usr/bin/env python3
from modules import Game, Config
import curses


def main(stdscr, config):
    game = Game(stdscr, config)
    game.play()
    return 0


if __name__ == '__main__':
    # boilerplate demon was sighted for 12 seconds
    import argparse
    import sys
    parser = argparse.ArgumentParser(
        prog="curdle.py"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument( "--daily",
        default=False,
        dest="daily",
        action="store_true",
        help="play word of the day")
    group.add_argument( "--custom",
        type=str,
        metavar="word",
        dest="word",
        action="store",
        help="specify word to play against")
    parser.add_argument( "--size",
        default=3,
        type=int,
        metavar="num",
        dest="size",
        action="store",
        help="maximum width of the window")
    parser.add_argument( "--tries",
        default=6,
        type=int,
        metavar="num",
        dest="tries",
        action="store",
        help="max number of guesses")
    parser.add_argument( "--secret",
        default=False,
        dest="secret",
        action="store_true",
        help="don't show solution if player loses")
    parser.add_argument( "--strict",
        default=False,
        dest="strict",
        action="store_true",
        help="use smaller wordlist for allowed guesses")
    # hidden options
    parser.add_argument( "--noborder",
        default=False,
        dest="no_border",
        action="store_true",
        help=argparse.SUPPRESS)
    # recommended with Konsole
    parser.add_argument( "--simplecolor",
        default=False,
        dest="simplecolor",
        action="store_true",
        help=argparse.SUPPRESS)
    parser.add_argument( "--layout",
        default="qwerty",
        choices=("qwerty", "azerty", "dvorak"),
        metavar="layout",
        dest="layout",
        help=argparse.SUPPRESS)
    args = parser.parse_args()
    # fatalities: 670.346

    config = Config
    if args.daily:
        config.setdaily()
    elif args.word:
        config.setsolution(args.word)
    if args.size:
        config.setwidth(args.size)
    if args.strict:
        config.strict()
    if args.secret:
        config.showsolution = False
    if args.tries:
        config.maxguesses = args.tries
    if args.no_border:
        config.drawborder = False
    if args.simplecolor:
        config.simplecolor = True
    if args.layout:
        config.setlayout(args.layout)

    try:
        sys.exit(curses.wrapper(main, config))
    except KeyboardInterrupt:
        sys.exit(0)
    except OverflowError:
        print("Couldn't start display.")
        print("Window needs to be at least 27x16")
        sys.exit(1)
