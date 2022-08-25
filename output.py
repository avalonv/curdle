import curses
from const import *
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


def end_score(screen, win:bool, result):
    if win:
        color_str(screen, 'You win!', 0, 5, Status.MATCH)
        color_str(screen, f'Score: {result}/{max_guesses}', 1, 4, Status.MATCH)
    else:
        color_str(screen, 'You lose!', 0, 4, Status.MISPLACE)
        color_str(screen, f'word: {result}', 1, 3, Status.MISPLACE)
    screen.refresh()
    sleep(2)
