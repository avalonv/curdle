import curses, curses.textpad
from const import *
from time import sleep


def color_str(screen, string, y, x, color=white):
    screen.addstr(y, x, string, curses.color_pair(color))


def color_char(screen, char, y, x, color=white, uppercase=True):
    if uppercase:
        char = char.upper()
    screen.addstr(y, x, char, curses.color_pair(color))


def update_words(screen, words, spacing):
    screen.clear()
    y = -1
    for word in words:
        y += 1
        x = 0
        for i in range(len(word[0])):
            char = word[0][i]
            color = word[1][i]
            color_char(screen, char, y, x, color)
            x += spacing + 1
    screen.refresh()


def update_kb(screen, kb_dic):
    screen.clear()
    y = 0
    for row in 'qwertyuio', 'asdfghjkl', '  zxcvbnm':
        x = 0
        for char in row:
            try:
                color = kb_dic[char]
            except KeyError: # spaces make it pissy
                color_char(screen, char, y, x)
                x += 1
                continue
            color_char(screen, char, y, x, color, False)
            x += 2
        y += 1
    screen.refresh()


def end_score(screen, win:bool, score=max_guesses):
    if win:
        color_str(screen, 'You win!', 0, 5, green)
        color_str(screen, f'Score: {score}/{max_guesses}', 1, 3, green)
    else:
        color_str(screen, 'You lose!', 0, 4, yellow)
        color_str(screen, f'word: {wordle}', 1, 3, yellow)
    screen.refresh()
    sleep(2)


def assign_win_geometry(stdscr, spacing, border=True):
    # a whole nightmare in the palm of your hand!
    max_y = curses.LINES - 1
    max_x = curses.COLS - 1
    middle_x = round(max_x / 2)

    score_width = len(wordle) * (spacing + 1)
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
        # this is relevant for the resizing loop, should
        # the border be drawn twice for whatever reason
        stdscr.clear()
        curses.textpad.rectangle(stdscr, border_start_y,
            border_start_x, border_end_y, border_end_x)
        color_str(stdscr, '  wordle  ', 0, middle_x-5, white)
        stdscr.refresh()
    return scorewin, msgwin, kbwin
