# curdle - A terminal wordle clone in curses

<p align="center">
  <img src="https://user-images.githubusercontent.com/29720696/194038280-b61c21cb-d2f0-4151-8f3d-5e84538720aa.png"/>
</p>

What it says on the tin. I made this primarily for self-education purposes to get reacquainted with programming. Most other command-line Wordle clones are also either really simple or incapable of running on small windows. This tries to strike a balance between features and not requiring external libraries.

## Installation
Requires Python 3.6 or higher.

Should not require any additional tools on \*nix systems (MacOS, Linux), simply clone this repository:

```sh
git clone https://github.com/avalonv/curdle
cd curdle
```

## Usage
By default, running `./curdle.py` will pick a word at random.

You can also play against the word of the day from the NYT version:

`./curdle.py --daily`

 or pass your own word as an argument:

`./curdle.py --custom [solution]`

the proverbial --help summary in place of good documentation:

```
options:
  -h, --help     show this help message and exit
  --daily        play word of the day
  --custom word  specify word to play against
  --size num     maximum width of the window
  --tries num    max number of guesses
  --secret       don't show solution if player loses
  ```

## Wordlists
Words to play against, and words which can be used as guesses are separate lists (with the latter being significantly larger) by default.

The provided valid-solutions list tries to track the NYT version of Wordle, and the valid-guesses list includes virtually all 5 letter words in English.

Both are available in modules/. Their contents can be made identical with `cat valid-solutions.txt > valid-guesses.txt` if preferred.

If creating a custom wordlist, valid-guesses should be equal or *greater* than valid-solutions. Doing it the other way around will break things.

- In theory, its logic should already support words of any length, as long as the appropriate lists are provided, but the interface will probably be misaligned.

### Windows
The built-in python curses module isn't supported on Windows.

Alternatives such as Uni-Curses seem unreliable, but I'd be willing to try a similar alternative if it exists.

#### TODO:
- [X] Allow passing of arguments for what the word should be

- [X] Maybe add nyt option which syncs with the official game's word of the day

- [X] Update word display logic to more closely match the original's when there are repeated letters

- [X] Expose more options as command line arguments

- [ ] Fix terrible colour contrast on some terminals

- [ ] Hard mode
