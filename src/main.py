import game, unit, user, reddit

"""
Main game controller
"""

def get_user(name, list):
    for user in list:
        if user.username is name:
            return user
    return None

def main():
    
    g = game.load_game()
    r = reddit.Reddit()
    us = []
    
    exit = False

    while (not exit):
        post = r.next_comment()
        
        u = get_user(post["user"], us)
        if u is None:
            u = user.User(post["user"])
            us.append(u)
                
        g.parse_command(u, post["comment"], r)

if __name__ == "__main__":
    main()