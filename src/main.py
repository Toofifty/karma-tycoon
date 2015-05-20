#!/user/bin/env pthon
"""
Karma Tycoon Bot
Main game controller
main.py

http://karma.matho.me/
"""

import game, reddit

def main():
    """Main function

    Instantiates game and reddit, and
    runs main loop.
    """

    reddit.Reddit().run_loop(game.Game())


if __name__ == "__main__":
    main()
