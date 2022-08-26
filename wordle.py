#!/usr/bin/env python3
from config import *
from sys import argv
import input as input
import output as out
import curses


def game(stdscr, solution, daily=False):
    out.set_colors()
    spacing = Config.MAXSPACING
    # this will catch the very useful and informative 'curses.error'
    # when attempting to create windows larger than the screen
    # (i.e. the whole terminal), and reduce the spacing between chars
    # (and thus size of the windows) until it fits. it will also catch
    # other, equally important errors, with equally informative names,
    # so it's best to call create_wins directly if debugging
    while True:
        if spacing >= 1:
            try:
                window_list = out.create_wins(stdscr, spacing, is_daily=daily)
                break
            except curses.error:
                spacing -= 1
        else:
            # window too small
            raise OverflowError
    scorewin, msgwin, kbwin = window_list

    kb_status = {letter:Status.MISMATCH for letter in Config.ALPHABET}
    guessed_words = []
    while len(guessed_words) < Config.MAXGUESSES:
        out.update_kb(kbwin, kb_status)
        guess = input.echo_str(scorewin, len(guessed_words), spacing)
        if guess in Config.VALIDWORDS:
            guess_status = input.compare_word(guess, solution, kb_status)
            guessed_words.append((guess, guess_status))
            scorewin.refresh()
            # only refresh 'word not in list'
            # message if a new input passes
            msgwin.clear()
            msgwin.refresh()
            if guess == solution:
                out.update_kb(kbwin, kb_status)
                out.update_words(scorewin, guessed_words, spacing)
                out.you_won(msgwin, len(guessed_words))
                stdscr.getkey()
                return 0
        else:
            out.color_str(msgwin, 'Word not in list.', 1, 0, Status.MISMATCH)
            msgwin.refresh()
        out.update_kb(kbwin, kb_status)
        out.update_words(scorewin, guessed_words, spacing)

    out.you_lose(msgwin, solution)
    stdscr.getkey()
    return 1


if __name__ == '__main__':
    solution = Config.RANDOMWORD
    daily = False
    if len(argv) > 1:
        arg = argv[1].rstrip().lower()
        if arg == "--nyt":
            solution = Config.DAILYWORD
            daily = True
        elif len(arg) == Config.WORDLEN and arg in Config.VALIDWORDS:
            solution = arg
        else:
            print(f"Word not in list")
            exit(2)
    try:
        exit(curses.wrapper(game, solution, daily))
    except KeyboardInterrupt:
        exit(0)
    except OverflowError:
        print("Couldn't start display.")
        print("Window needs to be at least 27x16")
        exit(2)
