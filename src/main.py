#!/user/bin/env pthon
"""
Karma Tycoon Bot
Main game controller
main.py

http://karma.matho.me/
"""

import game, unit, user, reddit

def get_user(name, list):
    """Get User object from list
    
    return user object or None
    """
    for user in list:
        if user.username is name:
            return user
    return None

def main():
    """Main function
    
    Instantiates game and reddit, and
    runs main loop.
    """
    g = game.Game()     # game object
    r = reddit.Reddit() # reddit object
    us = []             # (current) users list
    
    exit = False
    while (not exit):
        post = r.next_comment()
        # post has keys: "user", "comment"
        u = get_user(post["user"], us)
        if u is None:
            # create new user if not in list
            u = user.User(post["user"])
            us.append(u)
        
        # process comment, run action
        g.parse_command(u, post["comment"], r)

if __name__ == "__main__":
    main()