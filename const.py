import curses
from random import choice as random_choice

with open('./valid-wordle-words.txt', newline='') as wordle_file:
    w = random_choice(wordle_file.readlines())
    wordle = w.rstrip().lower()

# ideally the wordle_file should feature a smaller subset than
# the words_file, with only the latter including rare words
with open('./valid-input-words.txt', newline='') as words_file:
    words = words_file.readlines()
    valid_words = [w.rstrip().lower() for w in words]

max_guesses = 6
alphabet = {letter : 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
green = 3
yellow = 2
grey = 1
white = 0


def set_colors(inverted=False):
    # this might be important on some terminals, not on kitty or konsole
    curses.use_default_colors()
    if not inverted:
        # pair 0 is a constant and always points to the default fg/bg colors
        # related: on most systems I tested COLOR_BACK is actually grey
        curses.init_pair(green, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(grey, curses.COLOR_WHITE, curses.COLOR_BLACK)
    else:
        curses.init_pair(green, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(yellow, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(grey, curses.COLOR_BLACK, curses.COLOR_WHITE)
