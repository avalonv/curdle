from datetime import datetime as dt
from random import choice
from enum import IntEnum


class Status(IntEnum):
    MATCH = 3
    MISPLACE = 2
    MISMATCH = 1
    OTHER = 0


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
    # whether to invert colors
    INVERT = False
    # max space between letters, and thus the size of the interface. actual
    # space will vary based on screen size
    MAXSPACING = 3
    # max number of attempts before the game ends
    MAXGUESSES = 6
    # the layout of the keyboard shown on screen
    KBLAYOUT = Layout.QWERTY
    # where to look for words. note that solutions must be a subset of guesses
    _guesses_path = './valid-guesses.txt'
    _solutions_path = './valid-solutions.txt'

    # these you probably shouldn't touch
    with open('./valid-guesses.txt', newline='') as f1:
        lines = f1.readlines()
        VALIDWORDS = [w.rstrip().lower() for w in lines]

    with open('./valid-solutions.txt', newline='') as f2:
        lines = f2.readlines()
        VALIDSOLUTIONS = [w.rstrip().lower() for w in lines]
    SOLUTION = choice(VALIDSOLUTIONS)
    DAILYNUM = (dt.utcnow() - dt(2021, 6, 19)).days % len(VALIDSOLUTIONS)
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    DAILYWORD = VALIDSOLUTIONS[DAILYNUM]
    WORDLEN = len(SOLUTION)
    DAILY = False

    @classmethod
    def setdaily(cls):
        cls.DAILY = True
        cls.SOLUTION = cls.DAILYWORD

    @classmethod
    def setsolution(cls, new):
        cls.DAILY = False
        if new in cls.VALIDWORDS:
            cls.SOLUTION = new
        else:
            raise ValueError(f"'{new}' not in {cls._guesses_path}")
