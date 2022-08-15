#!/usr/bin/env python3
from sys import exit
from const import *
import logic, input
import output as out
import curses

# max space between letters, actual space depends on screen size
spacing = 3

def win_size_wrapper(stdscr):
    global spacing
    set_colors()
    # this will catch the very useful and informative 'curses.error'
    # when foolishly attempting to create windows larger than the
    # screen, and reduce the spacing between chars (and thus size
    # of the window) until it fits. it will also catch other,
    # equally helpful errors, with equally informative names,
    # so it's best to call set_win_geometry directly if debugging
    while True:
        if spacing >= 1:
            try:
                windows = out.assign_win_geometry(stdscr, spacing)
                break
            except curses.error:
                spacing -= 1
        else:
            raise OverflowError
    return windows


def game(stdscr):
    scorewin, msgwin, kbwin = win_size_wrapper(stdscr)

    guessed_words = []
    kb_dic = alphabet
    while len(guessed_words) < max_guesses:
        out.update_kb(kbwin, kb_dic)
        input_str = input.echo_str(scorewin, len(guessed_words), spacing)
        if logic.validate_word(input_str, valid_words):
            current_guess = logic.compare_word(input_str, wordle, kb_dic)
            guessed_words.append(current_guess)
            scorewin.refresh()
            msgwin.clear()
            msgwin.refresh()
            if current_guess[0] == wordle:
                out.update_kb(kbwin, kb_dic)
                out.update_words(scorewin, guessed_words, spacing)
                out.end_score(msgwin, win=True, score=len(guessed_words))
                stdscr.getkey()
                return 0
        else:
            out.color_str(msgwin, 'Word not in list.', 1, 0, grey)
            msgwin.refresh()
        out.update_kb(kbwin, kb_dic)
        out.update_words(scorewin, guessed_words, spacing)

    out.end_score(msgwin, win=False)
    stdscr.getkey()
    return 1


if __name__ == '__main__':
    try:
        exit(curses.wrapper(game))
    except KeyboardInterrupt:
        exit(2)
    except OverflowError:
        print("Couldn't start display, most likely your window is too small")
        exit(3)
