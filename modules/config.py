from datetime import datetime as dt
from random import choice
from enum import IntEnum
import os

_dirname = os.path.dirname(__file__)


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
    # where to look for words. note that solutions must be a subset of guesses
    _guesses_path = os.path.join(_dirname, 'valid-guesses.txt')
    _solutions_path = os.path.join(_dirname, 'valid-solutions.txt')
    # whether to draw a border & title around the screen
    border = True
    # whether to print the solution after losing a game
    showsolution = True
    # whether to invert colors
    invert = False
    # max space between letters, and thus the size of the interface. actual
    # space will vary based on screen size
    maxspacing = 3
    # max number of attempts before the game ends
    maxguesses = 6
    # the layout of the keyboard shown on screen
    kblayout = Layout.QWERTY
    # these you probably shouldn't touch
    with open(_guesses_path, newline='') as f1:
        lines = f1.readlines()
        validwords = [w.rstrip().lower() for w in lines]

    with open(_solutions_path, newline='') as f2:
        lines = f2.readlines()
        validsolutions = [w.rstrip().lower() for w in lines]
    solution = choice(validsolutions)
    dailynum = (dt.utcnow() - dt(2021, 6, 19)).days % len(validsolutions)
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    dailyword = validsolutions[dailynum]
    wordlen = len(solution)
    daily = False

    @classmethod
    def setdaily(cls):
        cls.daily = True
        cls.solution = cls.dailyword

    @classmethod
    def setsolution(cls, new):
        cls.daily = False
        new = new.lower()
        if new in cls.validwords:
            cls.solution = new
        else:
            raise ValueError(f"'{new}' not in {cls._guesses_path}")
