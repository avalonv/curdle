import curses
from config import *
from output import color_char
from collections import Counter


def echo_str(screen, start_y, spacing):
    # does no validation whatsoever except test that inputs are letters
    curses.curs_set(True) # turn the cursor on
    # process special keys as unique strings. while preferable
    # in that it sanitizes a bunch of annoying inputs, the side
    # effect is it returns strings too long for ord() :(
    screen.keypad(True)
    x = 0
    screen.move(start_y, x)
    max_x = Config.WORDLEN * (spacing + 1)
    user_string = ''
    # avoid not erasing characters if spacing is 0
    if spacing > 0:
        blanks = ' ' * spacing
    else:
        blanks = ' '

    while True:
        key = screen.getkey()
        if (key == 'KEY_ENTER' # switch statement dysphoria
            or key == '\n'):
            break
        # detecting a backspace was obnoxiously unreliable on kitty
        # check this if it doesn't work on other terminals:
        # https://stackoverflow.com/questions/47481955/
        elif (key == 'KEY_BACKSPACE'
              or key == '\b'
              or key == '\x7f'
              or key == 'KEY_DC'):
            # x keeps track of where characters should be displayed,
            # it can technically be inferred from len(user_string)
            # when we delete a word (backspace) we decrease x by the
            # amount of letterspacing (plus one), and print spaces over it
            if len(user_string) > 0:
                user_string = user_string[:-1]
                x -= spacing + 1
                color_char(screen, blanks, start_y, x)
        elif key.lower() in Config.ALPHABET:
            if len(user_string) < Config.WORDLEN:
                user_string += key
                color_char(screen, key.lower(), start_y, x)
                x += spacing + 1
        # another thing worthy of mention is that the cursor/caret
        # behaves like a ghost, its position is affected by output
        # functions, but it has no bearing where input actually goes.
        # this aligns it with the next input block so it's prettier
        if not x >= max_x:
            curses.curs_set(True)
            screen.move(start_y, x)
        else:
            # some terminals lack blinking cursors, so we disable it
            # on the max x so it doesn't overlap with the last letter
            curses.curs_set(False)

    curses.curs_set(False)
    return user_string


def compare_word(guess:str, solution:str, kb_status:dict):
    # initialize values as if all letters were wrong
    status = [Status.MISMATCH] * len(guess)
    # compute how often each letter appears in the solution
    solution_count = Counter(solution)
    # ... which we will then compare to matches in our guess
    matches = {letter : 0 for letter in Config.ALPHABET}
    # compare each letter in guess and solution, and set the
    # corresponding index to a match if they're equal
    for index, (letter1, letter2) in enumerate(zip(guess, solution)):
        if letter1 == letter2:
            status[index] = Status.MATCH
            matches[letter1] += 1

    # in a second pass, set letters to a misplace if they're in
    # the solution but at the wrond index. if they exceed the total
    # in the solution, purposefully ignore them. that is, if the
    # solution were 'walls', and guess 'lulls', treat the first 'l' as
    # a mismatch since the sum of matches for that letter is satisfied
    for index, (letter1, letter2) in enumerate(zip(guess, solution)):
        if letter1 != letter2 and solution_count[letter1] > matches[letter1]:
            status[index] = Status.MISPLACE

    # also check if the previous status for a letter was "higher"
    # before updating the keyboard, it may only increase
    for letter, value in zip(guess, status):
        if value > kb_status[letter]:
            kb_status[letter] = value

    return status
