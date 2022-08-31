# cursewordle - A terminal wordle clone in curses

![untitled](https://user-images.githubusercontent.com/29720696/185393916-d726b7a6-48bd-4e68-b632-31e7247d42c3.gif)

## Requirements
Requires python 3.1 or higher.

## Installation & Usage
Should not require any additional tools on \*nix systems (MacOS, Linux), simply clone this repository:

`git clone https://github.com/avalonv/cursewordle`

then `cd` into the new directory `cursewordle` and run:

`./wordle.py`

you can pass your own word as an argument, or play against the official word of the day from the NYT version of Wordle:

`./wordle.py --nyt`

## Configuration

Currently, there are a few hardcoded settings which can be manually adjusted in `config.py`. I plan to expose these as command line arguments eventually.

Any list of 5 letter words can be used, as long as `solution-list.txt` is equal to or contains a subset of `valid-inputs.txt`

In theory, its logic should already support words of any lenght, as long as the appropiate lists are provided, but it still requires more testing.

### Windows
The built-in python curses module isn't supported on Windows.

Alternatives such as Uni-Curses seem to be very unreliable, but I'd be willing to try a similar alternative if it exists.

#### TODO:
- [X] Allow passing of arguments for what the word should be

- [X] Maybe add nyt option which syncs with the official game's word of the day

- [X] Update word display logic to more closely match the original's when there are repeated letters

- [ ] Fix colour issues on some terminals

- [ ] Possibly also add option to print emoji summary at the end like the official game
