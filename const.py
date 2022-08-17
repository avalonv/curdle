import curses, curses.textpad
from datetime import datetime as dt
from random import choice as random_choice

# this includes almost all 5 letter words, which constitutes a much
# larger set than the one we sample wordle from
with open('./valid-words-extra.txt', newline='') as file1:
    lines = file1.readlines()
    valid_words = [w.rstrip().lower() for w in lines]

with open('./valid-words.txt', newline='') as file2:
    lines = file2.readlines()
    valid_answers = [w.rstrip().lower() for w in lines]

# the four horsemen of the apocalypse
max_guesses = 6
wordlen = len(valid_words[0])
alphabet = {letter : 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
daily_num = (dt.utcnow() - dt(2021, 6, 19)).days % len(valid_answers)

# and their mediocre siblings
green = 3
yellow = 2
grey = 1
white = 0


def set_random_wordle():
    wordle = random_choice(valid_answers)
    return wordle


def set_nyt_wordle():
    wordle = valid_answers[daily_num]
    return wordle


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


def set_win_size(stdscr, spacing, border=True, daily=False):
    # a whole nightmare in the palm of your hand!
    # realistically this doesn't have to be here. it's here
    # because it's unsightly and I don't want it anywhere else
    max_y = curses.LINES - 1
    max_x = curses.COLS - 1
    middle_x = round(max_x / 2)

    score_width = wordlen * (spacing + 1)
    score_height = max_guesses
    # try to align text with the middle of the screen
    # don't ask me why it works, I genuinely have no idea
    start_x =  round(middle_x - score_width / 2 + (spacing - 1) / 2 + 1)
    start_y = 2
    scorewin = curses.newwin(score_height, score_width, start_y, start_x)

    msg_width = 20
    msg_height = 2
    msg_start_y = start_y + score_height
    msg_start_x = middle_x - 8
    msgwin = curses.newwin(msg_height, msg_width, msg_start_y, msg_start_x)

    kb_width = 20
    kb_height = 3
    kb_start_y = msg_start_y + msg_height
    kb_start_x = middle_x - 8
    kbwin = curses.newwin(kb_height, kb_width, kb_start_y, kb_start_x)

    border_start_y = 0
    border_start_x = start_x - spacing - 8
    border_end_y = kb_start_y + kb_height + 1
    border_end_x = start_x + score_width + 7
    if border:
        title = '   wordle   '
        if daily:
            title = f'   wordle #{daily_num}   '
        title_start_x = middle_x - round(len(title) / 2)
        # this is relevant for the resizing loop, should the border
        # be drawn twice for whatever reason (happens sometimes)
        stdscr.clear()
        curses.textpad.rectangle(stdscr, border_start_y,
            border_start_x, border_end_y, border_end_x)
        stdscr.addstr(0, title_start_x, title, curses.color_pair(white))
        stdscr.refresh()
    return scorewin, msgwin, kbwin
