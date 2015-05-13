#!/user/bin/env pthon
"""
Karma Tycoon Bot
Main game controller
main.py

http://karma.matho.me/
"""

import time
import game, unit, user
import reddit, stats, history

def main():
    """Main function
    
    Instantiates game and reddit, and
    runs main loop.
    """
    g = game.Game()       # game object
    s = stats.Stats()     # stats object
    h = history.History() # history object
    r = reddit.Reddit()   # reddit object
    
    r.run_loop(g, s, h)
    

if __name__ == "__main__":
    main()