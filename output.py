import curses, curses.textpad
from config import *
from time import sleep


def color_str(screen, string, y, x, color=0):
    screen.addstr(y, x, string, curses.color_pair(color))


def color_char(screen, char, y, x, color=0, uppercase=True):
    if uppercase:
        char = char.upper()
    screen.addstr(y, x, char, curses.color_pair(color))


def update_words(screen, guesses, spacing):
# TODO: don't paint letters yellow if all the instances
# of that letter have already been identified as green
# for the current iteration.
# i.e. if the solution is 'omens' and the last guess was
# 'oozes', print the second 'o' as if it were grey to
# indicate there are no more instances of that letter
    screen.clear()
    y = -1
    for word in guesses:
        y += 1
        x = 0
        for i in range(len(word[0])):
            char = word[0][i]
            color = word[1][i]
            color_char(screen, char, y, x, color)
            x += spacing + 1
    screen.refresh()


def update_kb(screen, kb_status):
    screen.clear()
    y = 0
    for row in 'qwertyuio', 'asdfghjkl', '  zxcvbnm':
        x = 0
        for char in row:
            try:
                color = kb_status[char]
            except KeyError: # spaces make it pissy
                color_char(screen, char, y, x)
                x += 1
                continue
            color_char(screen, char, y, x, color, False)
            x += 2
        y += 1
    screen.refresh()


def end_score(screen, win:bool, result):
    if win:
        color_str(screen, 'You win!', 0, 5, Status.MATCH)
        color_str(screen, f'Score: {result}/{Config.MAXGUESSES}', 1, 4, Status.MATCH)
    else:
        color_str(screen, 'You lose!', 0, 4, Status.MISPLACE)
        color_str(screen, f'word: {result}', 1, 3, Status.MISPLACE)
    screen.refresh()
    sleep(2)


def set_colors(inverted=False):
    # this might be important on some terminals, not on kitty or konsole
    curses.use_default_colors()
    if not inverted:
        # pair 0 is a constant and always points to the default fg/bg colors
        # related: on most systems I tested COLOR_BACK is actually grey
        curses.init_pair(Status.MATCH, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Status.MISPLACE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(Status.MISMATCH, curses.COLOR_WHITE, curses.COLOR_BLACK)
    else:
        curses.init_pair(Status.MATCH, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(Status.MISPLACE, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(Status.MISMATCH, curses.COLOR_BLACK, curses.COLOR_WHITE)


def set_win_size(stdscr, spacing, border=True, daily=False):
    # a whole nightmare in the palm of your hand!
    # realistically this doesn't have to be here. it's here
    # because it's unsightly and I don't want it anywhere else
    max_y = curses.LINES - 1
    max_x = curses.COLS - 1
    middle_x = round(max_x / 2)

    score_width = Config.WORDLEN * (spacing + 1)
    score_height = Config.MAXGUESSES
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
            title = f'   wordle #{Config.DAILYNUM}   '
        title_start_x = middle_x - round(len(title) / 2)
        # this is relevant for the resizing loop, should the border
        # be drawn twice for whatever reason (happens sometimes)
        stdscr.clear()
        curses.textpad.rectangle(stdscr, border_start_y,
            border_start_x, border_end_y, border_end_x)
        color_str(stdscr, title, 0, title_start_x)
        stdscr.refresh()
    return scorewin, msgwin, kbwin
