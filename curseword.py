from sys import exit
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

# max space between letters, actual space depends on screen size
spacing = 3
max_guesses = 6
kb_colors = {letter : 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
wordle = 'dozen'


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


def print_str(stdscr, string, y, x, color=0):
    stdscr.addstr(y, x, string, curses.color_pair(color))


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
    max_x = len(wordle) * (spacing + 1)
    x = start_x
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
                print_char(screen, blanks, start_y, x, 0)
        elif key.lower() in kb_colors: # ignore things like arrow keys
            if i < len(wordle):
                string += key
                i += 1
                print_char(screen, key.lower(), start_y, x, 0)
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


def display_words(screen, words):
    # updates score_win with previous guesses as well
    # as the keyboard
    screen.clear()
    y = -1 # line/height
    for word in words:
        y += 1
        x = 0 # column/width
        for i in range(len(word[0])):
            char = word[0][i]
            color = word[1][i]
            print_char(screen, char, y, x, color)
            x += spacing + 1
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


def set_win_geometry(stdscr, border=True):
    # a whole nightmare in the palm of your hand!
    global scorewin, msgwin, kbwin
    max_y = curses.LINES - 1
    max_x = curses.COLS - 1
    middle_x = round(max_x / 2)

    score_width = len(wordle) * (spacing + 1)
    score_height = max_guesses
    # try to align text with the middle of the screen
    # don't ask me why it works, I genuinely have no idea
    start_x =  round(middle_x - score_width / 2 + (spacing - 1) / 2 + 1)
    start_y = 2
    scorewin = curses.newwin(score_height, score_width, start_y, start_x)

    msg_width = 20
    msg_height = 2
    msg_start_y = start_y + score_height
    msg_start_x = middle_x - 8
    msgwin = curses.newwin(msg_height, msg_width, msg_start_y, msg_start_x)

    kb_width = 20
    kb_height = 3
    kb_start_y = msg_start_y + msg_height
    kb_start_x = middle_x - 8
    kbwin = curses.newwin(kb_height, kb_width, kb_start_y, kb_start_x)

    if border:
        border_start_y = 0
        border_start_x = start_x - spacing - 8
        border_end_y = kb_start_y + kb_height + 1
        border_end_x = start_x + score_width + 7
        # this is relevant for the resizing loop, should
        # the border be drawn twice for whatever reason
        stdscr.clear()
        curses.textpad.rectangle(stdscr, border_start_y,
            border_start_x, border_end_y, border_end_x)
    stdscr.addstr(0, middle_x-5, '  wordle  ', curses.color_pair(0))
    stdscr.refresh()


def create_display(stdscr):
    global spacing
    set_colors()
    # this will catch the very useful and informative 'curses.error'
    # when foolishly attempting to create windows larger than the
    # screen, and reduce the spacing between chars (and thus size
    # of the window) until it fits. it will also catch other,
    # equally helpful errors, with equally informative names,
    # so it's best to call set_win_geometry directly for debugging
    while True:
        if spacing >= 1:
            try:
                set_win_geometry(stdscr)
                break
            except curses.error:
                spacing -= 1
        else:
            raise ValueError


def refresh_all():
    scorewin.refresh()
    msgwin.refresh()
    kbwin.refresh()

def game(stdscr):
    create_display(stdscr)

    guessed_words = []
    while len(guessed_words) < max_guesses:
        input_str = echo_read_string(scorewin, len(guessed_words), 0)
        if validate_input(scorewin, input_str):
            current_guess = compare_wordle(input_str)
            guessed_words.append(current_guess)
            scorewin.refresh()
            msgwin.clear()
            msgwin.refresh()
            if current_guess[0] == wordle:
                display_kb(kbwin)
                display_words(scorewin, guessed_words)
                print_str(msgwin, f'You win!', 0, 5, 3)
                print_str(msgwin, f'Score: {len(guessed_words)}/{max_guesses}',
                        1, 3, 3)
                msgwin.refresh()
                sleep(1)
                stdscr.getkey()
                return 0
        else:
            print_str(msgwin, f'Word not in list.', 1, 0, 1)
            msgwin.refresh()

        display_kb(kbwin)
        display_words(scorewin, guessed_words)
    print_str(msgwin, f'You lose!', 0, 4, 2)
    print_str(msgwin, f'word: {wordle}', 1, 3, 2)
    msgwin.refresh()
    sleep(3)
    stdscr.getkey()
    return 1


if __name__ == '__main__':
    try:
        exit(curses.wrapper(game))
    except KeyboardInterrupt:
        exit(2)
    except ValueError:
        print("Couldn't start display, most likely your window is too small")
        exit(3)
