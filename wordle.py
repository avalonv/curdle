#!/usr/bin/env python3
from config import *
from sys import argv
import input as input
import output as out
import curses

is_daily = False
# max space between letters, actual space depends on screen size
spacing = 3


def win_size_wrapper(stdscr):
    global spacing
    out.set_colors()
    # this will catch the very useful and informative 'curses.error'
    # when foolishly attempting to create windows larger than the
    # screen (i.e. the whole terminal), and reduce the spacing
    # between chars (and thus size of the windows) until it fits.
    # it will also catch other, equally important errors, with
    # equally informative names, so it's best to call set_win_size
    # directly if debugging
    while True:
        if spacing >= 1:
            try:
                windows = out.set_win_size(stdscr, spacing, True, is_daily)
                break
            except curses.error:
                spacing -= 1
        else:
            raise OverflowError
    return windows


def game(stdscr, solution):
    scorewin, msgwin, kbwin = win_size_wrapper(stdscr)

    guessed_words = []
    kb_status = {letter:Status.MISMATCH for letter in Config.ALPHABET}
    while len(guessed_words) < Config.MAXGUESSES:
        out.update_kb(kbwin, kb_status)
        guess = input.echo_str(scorewin, len(guessed_words), spacing)
        if guess in Config.VALIDWORDS:
            guess_status = input.compare_word(guess, solution, kb_status)
            guessed_words.append((guess, guess_status))
            scorewin.refresh()
            # only refresh 'word not in list'
            # message if new input passes
            msgwin.clear()
            msgwin.refresh()
            if guess == solution:
                out.update_kb(kbwin, kb_status)
                out.update_words(scorewin, guessed_words, spacing)
                out.end_score(msgwin, win=True, result=len(guessed_words))
                stdscr.getkey()
                return 0
        else:
            out.color_str(msgwin, 'Word not in list.', 1, 0, Status.MISMATCH)
            msgwin.refresh()
        out.update_kb(kbwin, kb_status)
        out.update_words(scorewin, guessed_words, spacing)

    out.end_score(msgwin, win=False, result=solution)
    stdscr.getkey()
    return 1


if __name__ == '__main__':
    solution = Config.RANDOMWORD
    if len(argv) > 1:
        arg = argv[1].rstrip().lower()
        if arg == "--nyt":
            solution = Config.DAILYWORD
            is_daily = True
        elif len(arg) == Config.WORDLEN and arg in Config.VALIDWORDS:
            solution = arg
        else:
            print(f"Word not in list")
            exit(2)
    try:
        exit(curses.wrapper(game, solution))
    except KeyboardInterrupt:
        exit(0)
    except OverflowError:
        print("Couldn't start display.")
        print("Window needs to be at least 27x16")
        exit(2)
