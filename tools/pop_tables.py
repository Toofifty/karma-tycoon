#!/user/bin/env pthon
"""
Karma Tycoon Bot
Test table populate class
pop_tables.py

http://karma.matho.me/
"""

import texter, game

# needs to be placed into /src/ to work.

def main():
    t = texter.Texter()
    g = game.Game()
    ts = t.pop_units_list(g.comment_units)
    with open("units_tables.txt", 'w') as f:
        f.write(ts)

if __name__ == "__main__":
    main()