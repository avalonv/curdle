# cursewordle - A terminal wordle clone in curses
![ezgif-5-9f47b7e1b2](https://user-images.githubusercontent.com/29720696/185168697-ead70f69-2386-4c82-a50b-3b661915123a.gif)


## Installation & Usage
Should not require any additional tools in modern \*nix systems, simply clone this repository:

`git clone https://github.com/avalonv/cursewordle`

then cd into the new directory and run:

`./wordle.py`

It also supports playing against the official daily Wordle from the NYT:

`./wordle.py --nyt`
####

## Windows
The built-in python curses module isn't available on Windows.

Alternatives such as Uni-Curses seem to be unreliable, so I don't plan to support it.

#### TODO:
Allow passing of arguments for what the word should be [Done]

Maybe add nyt option which syncs with the official game's word of the day [Done]

Update word display logic to more closely match the original's when there are repeated letters

Possibly also add option to print emoji summary at the end like the official game
