#!/user/bin/env pthon
"""
Karma Tycoon Bot
Main game controller
main.py

http://karma.matho.me/
"""

import game, unit, user, reddit

def main():
    """Main function
    
    Instantiates game and reddit, and
    runs main loop.
    """
    
    g = game.Game()       # game object
    r = reddit.Reddit()   # reddit object
    
    r.run_loop(g)
    

if __name__ == "__main__":
    main()