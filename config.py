from datetime import datetime as dt
from random import choice

# this includes almost all 5 letter words, which constitutes a much
# larger set than the one we sample solution from
with open('./valid-inputs.txt', newline='') as file1:
    lines = file1.readlines()
    input_list = [w.rstrip().lower() for w in lines]

with open('./solution-list.txt', newline='') as file2:
    lines = file2.readlines()
    solution_list = [w.rstrip().lower() for w in lines]


class Layout(tuple):
    AZERTY = (
            '  a z e r t y u i o p',
            ' q s d f g h j k l m j',
            '      w x c v b n')
    QWERTY = (
            ' q w e r t y u i o',
            ' a s d f g h j k l',
            '   z x c v b n m')
    DVORAK = (
            '     p y f g c r l',
            '  a o e u i d h t n s',
            '   q j k x b m w v z')


class Config():
    # whether to draw a border & title around the screen
    BORDER = True
    # whether to print the solution after losing a game
    SHOWSOLUTION = True
    # max space between letters, and thus the size of
    # the interface. actual space depends on screen size
    MAXSPACING = 3
    # max number of attempts before the game ends
    MAXGUESSES = 6
    # the layout of the keyboard shown on screen
    KBLAYOUT = Layout.QWERTY
    # these you probably shouldn't touch
    VALIDWORDS = input_list
    WORDLEN = len(VALIDWORDS[0])
    DAILYNUM = (dt.utcnow() - dt(2021, 6, 19)).days % len(solution_list)
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    RANDOMWORD = choice(solution_list)
    DAILYWORD = solution_list[DAILYNUM]


class Status(int):
    MATCH = 3
    MISPLACE = 2
    MISMATCH = 1
    OTHER = 0
