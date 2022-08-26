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


class Config():
    MAXGUESSES = 6
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
