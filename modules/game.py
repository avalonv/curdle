import curses, curses.textpad
from time import sleep
from collections import Counter
from .config import Config, Status


class Game():
    def __init__(self, stdscr, config=Config):
        self.CONST = config
        self.spacing:int = self.CONST.maxspacing
        windows = self._winsize_wrapper(stdscr)
        self.window_wrds = windows[0]
        self.window_msg = windows[1]
        self.window_kb = windows[2]
        self.guessed_words = []
        self.guessed_letters = {l:Status.OTHER for l in self.CONST.ALPHABET}


    def play(self):
        self._update_kb()
        while not self.gameover:
            if self.readguess() == self.CONST.solution:
                return self.display_victory()
        return self.display_loss()


    @property
    def gameover(self):
        if len(self.guessed_words) + 1 > self.CONST.maxguesses:
            return True
        else:
            return False


    @property
    def score(self):
        return f'{len(self.guessed_words)}/{self.CONST.maxguesses}'


    def display_victory(self):
        line1 = 'You win!'
        line2 = f'Score: {self.score}'
        Game._print_str(self.window_msg, line1, 0, 5, Status.MATCH)
        Game._print_str(self.window_msg, line2, 1, 4, Status.MATCH)
        self.window_msg.refresh()
        sleep(2)
        self.window_msg.getkey()
        return self.score


    def display_loss(self):
        line1 = 'You lose!'
        line2 = f'word: {self.CONST.solution}'
        Game._print_str(self.window_msg, line1, 0, 4, Status.MISPLACE)
        if self.CONST.showsolution:
            Game._print_str(self.window_msg, line2, 1, 3, Status.MISPLACE)
        self.window_msg.refresh()
        sleep(2)
        self.window_msg.getkey()
        return self.score


    def readguess(self):
        while True:
            rawstr = self._echo_read_keys().lower()
            if rawstr in self.CONST.validwords:
                current_guess = rawstr
                # only refresh 'word not in list'
                # message if a new input passes
                self.window_msg.clear()
                self.window_msg.refresh()
                break
            else:
                self._update_words()
                msg = 'Word not in list.'
                self.window_msg.clear()
                Game._print_str(self.window_msg, msg, 1, 0, Status.MISMATCH)
                self.window_msg.refresh()
        guess_status = self._compare_solution(rawstr)
        self.guessed_words.append((current_guess, guess_status))
        self._update_kb()
        self._update_words()
        return current_guess


    def _update_words(self):
        self.window_wrds.clear()
        y = -1
        for guess in self.guessed_words:
            y += 1
            x = 0
            for letter, status in zip(guess[0], guess[1]):
                Game._print_char(self.window_wrds, letter, y, x, status)
                x += self.spacing + 1
        self.window_wrds.refresh()


    def _update_kb(self):
        self.window_kb.clear()
        y = 0
        for row in self.CONST.kblayout:
            x = 0
            for letter in row:
                try:
                    status = self.guessed_letters[letter]
                # spaces make it pissy. move caret
                # forward as if one were typed
                except KeyError:
                    x += 1
                    continue
                Game._print_char(self.window_kb, letter, y, x, status, False)
                x += 1
            y += 1
        self.window_kb.refresh()


    def _compare_solution(self, guess:str):
        # initialize values as if all letters were wrong
        status = [Status.MISMATCH] * len(guess)
        # compute how often each letter appears in the solution
        solution_count = Counter(self.CONST.solution)
        # ... which we will then compare to matches in our guess
        matches = {letter : 0 for letter in self.CONST.ALPHABET}
        # compare each letter in guess and solution, and set the
        # corresponding index to a match if they're equal
        for index, (ltr1, ltr2) in enumerate(zip(guess, self.CONST.solution)):
            if ltr1 == ltr2:
                status[index] = Status.MATCH
                matches[ltr1] += 1
        # in a second pass, set letters to a misplace if they're in
        # the solution but at the wrond index. if they exceed the total
        # in the solution, purposefully ignore them. that is, if the
        # solution were 'walls', and guess 'lulls', treat the first 'l' as
        # a mismatch since the sum of matches for that letter is satisfied
        for index, (ltr1, ltr2) in enumerate(zip(guess, self.CONST.solution)):
            if ltr1 != ltr2 and solution_count[ltr1] > matches[ltr1]:
                status[index] = Status.MISPLACE
        # also check if the previous status for a letter was "higher"
        # before updating the keyboard, it may only increase
        for letter, value in zip(guess, status):
            if value > self.guessed_letters[letter]:
                self.guessed_letters[letter] = value
        return status


    def _echo_read_keys(self):
        # does no validation whatsoever except test that inputs are letters
        curses.curs_set(True) # turn the cursor on
        # process special keys as unique strings. while preferable
        # in that it sanitizes a bunch of annoying inputs, the side
        # effect is it returns strings too long for ord() :(
        self.window_wrds.keypad(True)
        x = 0
        start_y = len(self.guessed_words)
        self.window_wrds.move(start_y, x)
        max_x = self.CONST.wordlen * (self.spacing + 1)
        user_string = ''
        # avoid not erasing characters if spacing is 0
        if self.spacing > 0:
            blanks = ' ' * self.spacing
        else:
            blanks = ' '
        while True:
            key = self.window_wrds.getkey()
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
                # x = next character location, when we delete a word
                # (backspace) we decrease x by the amount of self.spacing
                # (plus one), and print spaces over it
                if len(user_string) > 0:
                    user_string = user_string[:-1]
                    x -= self.spacing + 1
                    Game._print_char(self.window_wrds, blanks, start_y, x)
            elif key.lower() in self.CONST.ALPHABET:
                if len(user_string) < self.CONST.wordlen:
                    user_string += key
                    Game._print_char(self.window_wrds, key.lower(), start_y, x)
                    x += self.spacing + 1
            # another thing worthy of mention is that the cursor/caret
            # behaves like a ghost, its position is affected by output
            # functions, but it has no bearing where input actually goes.
            # this aligns it with the next input block so it's prettier
            if not x >= max_x:
                curses.curs_set(True)
                self.window_wrds.move(start_y, x)
            else:
                # some terminals lack blinking cursors, so we disable it
                # on the max x so it doesn't overlap with the last letter
                curses.curs_set(False)
        curses.curs_set(False)
        return user_string


    def _winsize_wrapper(self, stdscr):
        # this will catch the very useful and informative 'curses.error' when
        # attempting to create windows larger than the screen (i.e. the whole
        # terminal), and reduce the spacing between chars (and thus size of the
        # windows) until it fits. it will also catch other, equally important
        # errors, with equally informative names, so it's best to call
        # create_wins directly if debugging curses itself
        while True:
            if self.spacing >= 1:
                try:
                    window_list = self._create_wins(stdscr)
                    break
                except curses.error:
                    self.spacing -= 1
            else:
                # https://twitter.com/S0phie_S0pht/status/1570506344284950528
                raise OverflowError
        return window_list


    def _create_wins(self, stdscr):
        # a whole nightmare in the palm of your hand!
        Game._set_colors(self.CONST.invert)
        max_y = curses.LINES - 1
        max_x = curses.COLS - 1
        mid_x = round(max_x / 2)

        wrds_width = self.CONST.wordlen * (self.spacing + 1)
        wrds_height = self.CONST.maxguesses
        # try to align text with the middle of the screen
        # don't ask me how it works, I genuinely have no idea
        start_x =  round(mid_x - wrds_width / 2 + (self.spacing - 1) / 2 + 1)
        start_y = 2
        win_wrds = curses.newwin(wrds_height, wrds_width, start_y, start_x)

        msg_width = 20
        msg_height = 2
        msg_start_y = start_y + wrds_height
        msg_start_x = mid_x - 8
        win_msg = curses.newwin(msg_height, msg_width, msg_start_y, msg_start_x)

        kb_width = 20 + 2
        kb_height = 3
        kb_start_y = msg_start_y + msg_height
        kb_start_x = round(mid_x - (len(max(self.CONST.kblayout, key=len)) + 1) / 2)
        win_kb = curses.newwin(kb_height, kb_width, kb_start_y, kb_start_x)

        border_start_y = 0
        border_start_x = start_x - self.spacing - 8
        border_end_y = kb_start_y + kb_height + 1
        border_end_x = start_x + wrds_width + 7
        if self.CONST.border:
            title = '   wordle   '
            if self.CONST.daily:
                title = f'   wordle #{self.CONST.dailynum}   '
            title_start_x = mid_x - round(len(title) / 2)
            # this clear() is relevant for the resizing loop, should the
            # border be drawn twice for whatever reason (happens sometimes)
            stdscr.clear()
            curses.textpad.rectangle(stdscr, border_start_y,
                border_start_x, border_end_y, border_end_x)
            Game._print_str(stdscr, title, 0, title_start_x)
            stdscr.refresh()
        return win_wrds, win_msg, win_kb


    @classmethod
    def _set_colors(cls, inverted=False):
        # this might be important on some terminals, not on kitty or konsole
        curses.use_default_colors()
        if not inverted:
            # pair 0 is a constant and always points to the default fg/bg colors
            # related: on most systems I tested COLOR_BACK is actually grey
            curses.init_pair(Status.MATCH, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(Status.MISPLACE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(Status.MISMATCH, curses.COLOR_WHITE, curses.COLOR_BLACK)
        else:
            curses.init_pair(Status.MATCH, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(Status.MISPLACE, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(Status.MISMATCH, curses.COLOR_BLACK, curses.COLOR_WHITE)


    @classmethod
    def _print_str(cls, screen, string, y, x, color=0):
        screen.addstr(y, x, string, curses.color_pair(color))


    @classmethod
    def _print_char(cls, screen, char, y, x, color=0, uppercase=True):
        if uppercase:
            char = char.upper()
        screen.addstr(y, x, char, curses.color_pair(color))
