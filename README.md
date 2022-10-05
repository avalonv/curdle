# curdle - A terminal wordle clone in curses

<p align="center">
  <img src="https://user-images.githubusercontent.com/29720696/193329907-66216dad-d86d-4652-94d4-aaa6a8201ffc.png" height="300"/>
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

`./curdle.py [solution]`

## Configuration
Words to play against, and words which can be used as guesses are separate lists (with the latter being significantly larger) by default. Both are available in modules/, their contents can be made identical with `cat valid-solutions.txt > valid-guesses.txt` if preferred.

There are a few other hardcoded options which can be manually adjusted in config.py, such as the keyboard layout and whether to hide the solution at the end.

- In theory, its logic should already support words of any length, as long as the appropriate lists are provided, but it still requires more testing.

### Windows
The built-in python curses module isn't supported on Windows.

Alternatives such as Uni-Curses seem unreliable, but I'd be willing to try a similar alternative if it exists.

#### TODO:
- [X] Allow passing of arguments for what the word should be

- [X] Maybe add nyt option which syncs with the official game's word of the day

- [X] Update word display logic to more closely match the original's when there are repeated letters

- [ ] Fix terrible colour contrast on some terminals

- [ ] Expose more options as command line arguments

- [ ] Hard mode
