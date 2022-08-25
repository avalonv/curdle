import curses
from const import *
from output import color_char
from collections import Counter, defaultdict


def echo_str(screen, start_y, spacing):
    # does no validation whatsoever except test that inputs are letters
    curses.curs_set(True) # turn the cursor on
    # while desirable, in that it sanitizes a bunch of
    # annoying inputs, it also produces strings too long
    # for ord(), which might fuck up handling of other keys
    screen.keypad(True) # process special keys as unique strings
    x = 0
    screen.move(start_y, x)
    max_x = word_len * (spacing + 1)
    user_str = ''
    i = 0
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
            # TL;DR is x determines where the input goes, and we use
            # i to keep track of how many characters were actually typed
            # (although in practice you can infer one from the other),
            # when we delete a word (backspace) we reduce i by one
            # and x by the amount of letterspacing plus one, and we
            # print as many spaces (blanks) as needed to also clear
            # whatever was left between those chars as a result of
            # shitty input handling (curses is an apt name)
            if i > 0:
                user_str = user_str[:-1]
                i -= 1
                x -= spacing + 1
                color_char(screen, blanks, start_y, x)
        elif key.lower() in alphabet: # ignore things like arrow keys
            if i <word_len:
                user_str += key
                i += 1
                color_char(screen, key.lower(), start_y, x)
                x += spacing + 1
        # another thing worthy of mention is that the cursor/caret
        # behaves like a ghost, its position is affected by output
        # functions, but it has no bearing where input actually goes.
        # this aligns it with the next input stream so it's prettier,
        # but it's not necessary for the rest to work.
        if not x >= max_x:
            curses.curs_set(True)
            screen.move(start_y, x)
        else:
            # some terminals lack blinking cursors, so
            # disable it on the max x so it doesn't
            # overlap with the last letter
            curses.curs_set(False)

    curses.curs_set(False)
    return user_str


def compare_word(guess, solution, kb_dic=alphabet):
    # this loop compares the chars in 'string' and 'solution' based on index,
    # and assigns a color to the respective index in the color array. so
    # if string were 'weiss', and solution were 'white', this function would
    # return something like this: ['weiss', [1,2,1,3,3]].
    # the structure for this is [string literal, [list of ints
    # referencing an assigned color]]. since the same letter can appear
    # multiple times in a word, we prefer to use the index i as a key
    # instead of a real dictionary, where repeated letters would all
    # point to the same color regardless of location.
    matches = guess, [0 for c in guess] # actually a list >_>
    green_c_count = defaultdict(int) # creates keys if they don't exist
    for i in range(len(matches[0])):
            char = matches[0][i]
            if char == solution[i]:
                color = Status.MATCH
                green_c_count[char] += 1
            elif char in solution:
                color = Status.MISPLACE
            else:
                color = Status.MISMATCH
            matches[1][i] = color
            # this ensures 'better' colors have priority, i.e.
            # a previously green letter can't become yellow
            if kb_dic[char] < color:
                kb_dic[char] = color
    string_c_count = Counter(guess)
    solution_c_count = Counter(solution)
    for k, v in green_c_count.items():
        if v == solution_c_count[k]:
            if string_c_count[k] > solution_c_count[k]:
                for i in range(len(matches[0])):
                    char = matches[0][i]
                    if char == k and matches[1][i] == Status.MISPLACE:
                        matches[1][i] = Status.MISMATCH
    return matches
