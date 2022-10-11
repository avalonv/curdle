# curdle

<p align="center">
  <img src="https://user-images.githubusercontent.com/29720696/194192473-a087d0d2-7e13-4163-84fe-f99cd9d5fe35.gif"/>
</p>

Wordle in curses. I made this primarily for self-education purposes to get reacquainted with programming. Most other command-line Wordle clones are also either really simple or incapable of running on small windows. This tries to strike a balance between features and maximum usability in a typical cli enviroment (without requiring external libraries).

## Installation
Requires Python 3.6 or higher.

Should not require any additional tools on \*nix systems (MacOS, Linux), simply clone this repository:

```sh
git clone https://github.com/avalonv/curdle
cd curdle
```

## Usage
By default, running `./curdle.py` will pick a word at random.

You can also play against the word of the day from the NYT version like so:

`./curdle.py --daily`

see the proverbial --help summary for other options:

```
options:
  --custom word  specify word to play against
  --size num     maximum width of the window
  --tries num    max number of guesses
  --secret       don't show solution if player loses
  --strict       use smaller wordlist for allowed guesses
  --simplecolor  fallback palette for terminals such as Konsole
  ```
## Wordlists
Words to play against, and words which can be used as guesses are stored as separate lists (with the latter being significantly larger) by default. Both are available in modules/.

The provided valid-solutions list *tries* to track the NYT version of Wordle, while the valid-guesses list includes virtually every 5 letter word in English.

Their contents can be made identical with `cat valid-solutions.txt > valid-guesses.txt` if preferred for whatever reason, although `--strict` achieves the same thing non-destructively.

If creating a custom wordlist, valid-guesses should be equal or *greater* than valid-solutions. Doing it the other way around will break things.

- In theory, its logic should already support words of any length, as long as the appropriate lists are provided. In practice there's a good chance the interface will be completely fucked up.

### Windows
The built-in python curses module isn't supported on Windows :(

Alternatives such as Uni-Curses seem unreliable, but I'd be willing to try a similar alternative if it exists.

#### TODO:
- [X] Allow passing of arguments for what the word should be

- [X] Maybe add nyt option which syncs with the official game's word of the day

- [X] Update word display logic to more closely match the original's when there are repeated letters

- [X] Expose more options as command line arguments

- [X] Fix terrible colour contrast on some terminals

- [ ] Hard mode
