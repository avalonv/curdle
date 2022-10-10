from datetime import datetime as dt
from random import choice
from enum import IntEnum
import os

DIRNAME = os.path.dirname(__file__)


class Status(IntEnum):
    MATCH = 3
    MISPLACE = 2
    MISMATCH = 1
    OTHER = 0


class Config():
    _LAYOUTS = {'azerty':
                (
                '  a z e r t y u i o p',
                ' q s d f g h j k l m j',
                '      w x c v b n'),
                'qwerty':
                (
                ' q w e r t y u i o p',
                '  a s d f g h j k l',
                '    z x c v b n m'),
                'dvorak':
                (
                '    p y f g c r l',
                ' a o e u i d h t n s',
                '  q j k x b m w v z') }
    _GUESSES_PATH = os.path.join(DIRNAME, 'valid-guesses.txt')
    _SOLUTIONS_PATH = os.path.join(DIRNAME, 'valid-solutions.txt')
    with open(_GUESSES_PATH, newline='') as f1:
        lines = f1.readlines()
        validwords = [w.rstrip().lower() for w in lines]
    with open(_SOLUTIONS_PATH, newline='') as f2:
        lines = f2.readlines()
        validsolutions = [w.rstrip().lower() for w in lines]
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    DAILYNUM = (dt.utcnow() - dt(2021, 6, 19)).days % len(validsolutions)
    DAILYWORD = validsolutions[DAILYNUM]
    daily = False
    solution = choice(validsolutions)
    wordlen = len(solution)
    showsolution = True
    drawborder = True
    simplecolor = False
    maxspacing = 3
    maxguesses = 6
    kblayout = _LAYOUTS['qwerty']


    @classmethod
    def setdaily(cls):
        cls.daily = True
        cls.solution = cls.DAILYWORD


    @classmethod
    def setsolution(cls, new):
        cls.daily = False
        new = new.lower()
        if new in cls.validwords:
            cls.solution = new
        else:
            raise ValueError(f"'{new}' not in {cls._GUESSES_PATH}")


    @classmethod
    def setwidth(cls, new):
        if new > 0:
            cls.maxspacing = new
        else:
            raise ValueError("Width must be bigger than 0")


    @classmethod
    def setlayout(cls, new):
        keys = cls._LAYOUTS.keys()
        if new in keys:
            cls.kblayout = cls._LAYOUTS[new]
        else:
            raise ValueError(f"'{new}' not in {keys}")


    @classmethod
    def strict(cls):
        if cls.solution in cls.validsolutions:
            cls.validwords = cls.validsolutions
        else:
            raise ValueError(f"'{cls.solution}' not in {cls._SOLUTIONS_PATH}")
