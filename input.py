import curses
from const import *
from output import color_char


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
    string = ''
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
                string = string[:-1]
                i -= 1
                x -= spacing + 1
                color_char(screen, blanks, start_y, x)
        elif key.lower() in alphabet: # ignore things like arrow keys
            if i <word_len:
                string += key
                i += 1
                color_char(screen, key.lower(), start_y, x)
                x += spacing + 1
        # another thing worthy of mention is that the cursor/caret
        # behaves like a ghost, its position is affected by output
        # functions, but it has no bearing where input actually goes.
        # this aligns it with the next input stream so it's prettier,
        # but it's not necessary for the rest to work.
        if not x >= max_x:
            screen.move(start_y, x)
        else:
            screen.move(start_y, x - spacing - 1)

    curses.curs_set(False)
    return string


def compare_word(string, wordle, kb_dic):
    # this loop compares the chars in 'string' and 'wordle' based on index,
    # and assigns a color to the respective index in the color array. so
    # if string were 'weiss', and wordle were 'white', this function would
    # return something like this: ['weiss', [1,2,1,3,3]].
    # the structure for this is [string literal, [list of ints
    # referencing an assigned color]]. since the same letter can appear
    # multiple times in a word, we prefer to use the index i as a key
    # instead of a real dictionary, where repeated letters would all
    # point to the same color regardless of location.
    word_dic = string, [0 for c in string] # actually a list >_>
    for i in range(len(word_dic[0])):
            char = word_dic[0][i]
            if char == wordle[i]:
                color = green
            elif char in wordle:
                color = yellow
            else:
                color = grey
            word_dic[1][i] = color
            # this ensures 'better' colors have priority, i.e.
            # a previously green letter can't become yellow
            if kb_dic[char] < color:
                kb_dic[char] = color
    return word_dic
