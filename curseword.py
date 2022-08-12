from time import sleep
from random import choice as random_choice
import curses, curses.textpad

with open('./valid-wordle-words.txt', newline='') as wordle_file:
    w = random_choice(wordle_file.readlines())
    wordle = w.rstrip().lower()

# ideally the wordle_file should feature a smaller subset than
# the words_file, with only the latter including rare words
with open('./valid-input-words.txt', newline='') as words_file:
    words = words_file.readlines()
    valid_words = [w.rstrip().lower() for w in words]

wordle = 'dozen'
letterspacing = 2 # changing this might cause some alignment issues
max_guesses = 6
kb_colors = {letter : 0 for letter in 'qwertyuiopasdfghjklzxcvbnm'}

def set_colors(inverted=False):
    # this might be important on some terminals, not on kitty or konsole
    curses.use_default_colors()
    # curses.COLOR can only be invoked after stdscr has been created,
    # and ours is wrapped and I'm too lazy to read the documentation,
    # so this function's main purpose is uncluttering main
    if not inverted:
        # pair 0 is a constant and always points to the default fg/bg colors
        # related: on most systems I tested COLOR_BACK is actually grey
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    else:
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


def print_char(stdscr, char, y, x, color=0, uppercase=True):
    if uppercase:
        char = char.upper()
    stdscr.addstr(y, x, char, curses.color_pair(color))


def echo_read_string(screen, start_y, start_x):
    curses.curs_set(True) # turn the cursor on
    # while desirable, in that it sanitizes a bunch of
    # annoying inputs, it also produces strings too long
    # for ord(), which might fuck up handling of other keys
    screen.keypad(True) # process special keys as unique strings
    screen.move(start_y, start_x)
    max_x = len(wordle) * (letterspacing + 1)
    x = start_x
    string = ''
    i = 0
    # avoid not erasing characters if spacing is 0
    if letterspacing > 0:
        blanks = ' ' * letterspacing
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
            # this is kinda complicated, but the TL;DR is x
            # determines where the input goes, and we use i to keep
            # track of how many characters were actually typed
            # (although in practice you can infer one from the other),
            # when we delete a word (backspace) we reduce i by one
            # and x by the amount of letterspacing plus one, and we
            # print as many spaces (blanks) as needed to also clear
            # whatever was left between those chars as a result of
            # shitty input handling (curses is an apt name)
            if i > 0:
                string = string[:-1]
                i -= 1
                x -= letterspacing + 1
                print_char(screen, blanks, start_y, x, 0)
        elif key.lower() in kb_colors: # ignore things like arrow keys
            if i < len(wordle):
                string += key
                i += 1
                print_char(screen, key.lower(), start_y, x, 0)
                x += letterspacing + 1
        # another thing worthy of mention is that the cursor/caret
        # is much like a ghost, its position is affected by output
        # functions, but it has no bearing where input actually goes.
        # this aligns it with the next input stream so it's prettier,
        # but it's not necessary for the rest to work.
        if not x >= max_x:
            screen.move(start_y, x)
        else:
            screen.move(start_y, x - letterspacing - 1)

    curses.curs_set(False)
    return string


def compare_wordle(string):
    global kb_colors
    # the structure for this is [string literal, [list of ints
    # referencing an assigned color]]. since the same letter can appear
    # multiple times in a word, we prefer to use the index i as a key
    # instead of a real dictionary, where repeated letters would all
    # point to the same color regardless of location.
    word_dic = string, [0 for c in string] # actually a list >_>
    # this loop compares the chars in 'string' and 'wordle' based on index,
    # and assigns a color to the respective index in the color array. so
    # if string were 'weiss', and wordle were 'white', this function would
    # return something like this: ['weiss', [1,2,1,3,3]]
    # TODO: also set the alphabet colors in this loop
    for i in range(len(word_dic[0])):
            char = word_dic[0][i]
            if char == wordle[i]:
                color = 3 # green
            elif char in wordle:
                color = 2 # yellow
            else:
                color = 1 # grey
            word_dic[1][i] = color
            # this ensures 'better' colors have priority, i.e.
            # a previously green letter can't become yellow
            if kb_colors[char] < color:
                kb_colors[char] = color
    return word_dic


def validate_input(screen, string):
    # this actually tests whether input is a valid word, since
    # echo_get_word just sanitizes for random bullshit like numbers
    # TODO: actually print the not in the wordlist message (preferably)
    # in a different window
    if len(string) != len(wordle):
        return False
    elif string not in valid_words:
        # print(f"Not in the wordlist")
        return False
    else:
        return True


def display_words(screen, words, start_y, start_x):
    # updates score_win with previous guesses as well
    # as the keyboard
    screen.clear()
    y = start_y - 1 # line/height
    for word in words:
        y += 1
        x = start_x # column/width
        for i in range(len(word[0])):
            char = word[0][i]
            color = word[1][i]
            print_char(screen, char, y, x, color)
            x += letterspacing + 1
    screen.refresh()


def display_kb(screen):
    screen.clear()
    y = 0
    for row in 'qwertyuio', 'asdfghjkl', '  zxcvbnm':
        x = 0
        for char in row:
            try:
                color = kb_colors[char]
            except KeyError:
                print_char(screen, char, y, x)
                x += 1
                continue
            print_char(screen, char, y, x, color, False)
            x += 2
        y += 1
    screen.refresh()


def initialize_screens(stdscr, border=True):
    # a whole nightmare in the palm of your hand!
    global scorewin, kbwin
    max_y = curses.LINES - 1
    max_x = curses.COLS - 1
    middle_x = max_x / 2

    score_width = len(wordle) * (letterspacing + 1)
    score_height = max_guesses
    start_x = round(middle_x - (score_width / 2)) + 1
    start_y = 1
    scorewin = curses.newwin(score_height, score_width, start_y, start_x)

    # adjusted to align with middle row of score_win (it's messy)
    adjst_middle = start_x + round((len(wordle) * letterspacing + 1) / 2) + 2
    kb_width = 20
    kb_height = 3
    kb_start_y = start_y + score_height + 2
    kb_start_x = adjst_middle - 10
    kbwin = curses.newwin(kb_height, kb_width, kb_start_y, kb_start_x)

    border_start_y = start_y - 1
    border_start_x = start_x - letterspacing - 8
    border_end_y = kb_start_y + 4
    border_end_x = start_x + score_width + 7
    if border:
        curses.textpad.rectangle(stdscr, border_start_y,
            border_start_x, border_end_y, border_end_x)
        stdscr.refresh()


def game(stdscr):
    set_colors()
    initialize_screens(stdscr)

    guessed_words = []
    while len(guessed_words) < max_guesses:
        input_str = echo_read_string(scorewin, len(guessed_words), 0)
        if validate_input(scorewin, input_str):
            current_guess = compare_wordle(input_str)
            guessed_words.append(current_guess)
            if current_guess[0] == wordle:
                display_kb(kbwin)
                display_words(scorewin, guessed_words, 0, 0)
                print('win')
                sleep(3)
                return
        display_kb(kbwin)
        display_words(scorewin, guessed_words, 0, 0)
    print('lose')
    sleep(3)

if __name__ == '__main__':
    curses.wrapper(game)
