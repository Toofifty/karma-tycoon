#!/user/bin/env pthon
"""
Karma Tycoon Bot
SQL Database interface functions
db.py

http://karma.matho.me/
"""

import sqlite3, time

con = sqlite3.connect("../data/kt.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

def init():
    """Create tables"""
    
    with con:    
        cur.execute("CREATE TABLE users(name TEXT, title TEXT, gold INT, \
                link_karma INT, comment_karma INT)")
        cur.execute("CREATE TABLE units(id INT, type TEXT, name TEXT, \
                short TEXT, amount INT, init_cost INT, init_profit INT, \
                init_time INT)")
        cur.execute("CREATE TABLE commands(id INTEGER PRIMARY KEY, \
                username TEXT, command TEXT, type TEXT, unit_id TEXT, \
                value INT, time_sec INT)")
        cur.execute("CREATE TABLE game(id INTEGER PRIMARY KEY, gold INT, \
                link_karma INT, comment_karma INT, lifetime_lk INT, \
                lifetime_ck INT, runtime INT)")
        cur.execute("CREATE TABLE comments(id INT)")
                
    
def new_game():
    """Adds a new game record"""

    confirm = raw_input(":: are you sure you wish to reset the game? (y/n)")
    if confirm != "y":
        return
        
    with con:
        cur.execute("SELECT * FROM game")
        games = cur.fetchall()
        if games is None:
            id = 0
        else:
            id = len(games)
        cur.execute("INSERT INTO game VALUES(?, 0, 0, 0, 0, 0, 0)", (id,))
    
    
def get_game():
    """Get current game info"""

    with con:
        cur.execute("SELECT * FROM game ORDER BY id DESC")
        game = cur.fetchone()
        if game is None:
            print ":: no game save found"
            print ":: creating new..."
            new_game()
            return get_game()
            
        return game
        
        
def update_game(game):
    """Saved the game state"""

    values = (game.gold, game.link_karma, game.comment_karma, 
            game.lifetime_lk, game.lifetime_ck, 
            game.runtime + time.time() - self.session_start)

    with con:
        cur.execute("UPDATE game SET gold=? link_karma=? comment_karma=? \
                lifetime_lk=? lifetime_ck=? runtime=?", values)
    
                
def get_users():
    """Gets all the users"""

    with con:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
        
                
def get_user(username):
    """Get the user data for username"""

    with con:
        cur.execute("SELECT * FROM users WHERE name=?", (username,))
        
        user = cur.fetchone()
        
        if user is None:
            print ":: creating new user %s" % username
            cur.execute("INSERT INTO users VALUES(?, '', 0, 0, 0)",
                    (username,))
            return get_user(username)
        
        return user
    
        
def update_user(user):
    """Updates a user record."""
    
    values = (user.name, user.title, user.gold, user.link_karma, 
                user.comment_karma)
    with con:
        cur.execute("UPDATE users SET title=? gold=? link_karma=? \
                    comment_karma=? WHERE name=?", values[1:] + values[:1])
        
        
def get_units(type):
    with con:
        cur.execute("SELECT * FROM units WHERE type=?", (type,))
        return cur.fetchall()
        

def get_unit(id):
    with con:
        cur.execute("SELECT 1 FROM units WHERE id=?", (id,))
        return cur.fetchone()
        

def add_command(user, command, type, unitID, value):
    with con:
        cur.execute("INSERT INTO commands(username, command, type, unit_id, \
                    value, time) VALUES(?, ?, ?, ?, ?, ?)", (user.name,
                    command, type, unitID, value, 
                    time.time()))
                    
                    
def get_command_count(user):
    with con:
        cur.execute("SELECT * FROM commands WHERE username=?", (user.name,))
        return len(cur.fetchall())
        
def add_comment_id(id):
    with con:
        cur.execute("INSERT INTO comments(id) VALUES(?)", (id,))
        
        
def has_comment_id(id):
    with con:
        cur.execute("SELECT * FROM comments WHERE id=?", (id,))
        return not cur.fetchone() is None
        
        
def get_position(user):
    with con:
        cur.execute("SELECT * FROM users WHERE ? < link_karma + comment_karma", 
                (user.get_total_karma(),))
        print len(cur.fetchall()) + 1

        
def get_top_karma_type(type, amount, hours):
    """Gets _amount_ top users for karma _type_
    in last _hours_ hours.
    
    If hours is None, gets total karma
    """

    with con:
        if hours is None:
        
            cur.execute("SELECT * FROM users ORDER BY ? DESC", (type,))
            return cur.fetchall()[:amount]
            
        elif "+" in type:
       
            cur.execute("SELECT * FROM commands WHERE time_sec > ? \
                    AND command=? AND (type=? OR type=?)", 
                    (time.time() - hours * 3600, "post", "link", "comment"))
                    
            tally = {}
            tally_link = {}
            tally_comment = {}
            for command in cur.fetchall():
                # tally both for ordering
                if not command["username"] in tally:
                    tally[command["username"]] = command["value"]
                else:
                    tally[command["username"]] += command["value"]
                
                # tally each for output
                if command["type"] == "link":
                    if not command["username"] in tally_link:
                        tally_link[command["username"]] = command["value"]
                    else:
                        tally_link[command["username"]] += command["value"]
                        
                else:
                    if not command["username"] in tally_comment:
                        tally_comment[command["username"]] = command["value"]
                    else:
                        tally_comment[command["username"]] += command["value"]
                        
            # sort and place into list
            top_in_hours = []
            for p in sorted(tally, key=tally.get, reverse=True):
                top_in_hours.append({"name":p, 
                        "link_karma":tally_link[p], 
                        "comment_karma":tally_comment[p]})
                        
            return top_in_hours[:amount]
            
        else:
        
            type = type.replace("_karma", "")
        
            cur.execute("SELECT * FROM commands WHERE time_sec > ? \
                    AND command=? AND type=?", (time.time() - hours * 3600,
                    "post", type))
            
            tally = {}
            for command in cur.fetchall():
                if not command["username"] in tally:
                    tally[command["username"]] = command["value"]
                else:
                    tally[command["username"]] += command["value"]
                
            # sort and place into list
            top_in_hours = []
            for p in sorted(tally, key=tally.get, reverse=True):
                top_in_hours.append({"name":p, type + "_karma":tally[p]})
                
            return top_in_hours[:amount]
            
    
def get_top_karma(amount, hours=None):
    return get_top_karma_type("link_karma + comment_karma", amount, hours)
    
    
def get_top_link_karma(amount, hours=None):
    return get_top_karma_type("link_karma", amount, hours)
    
    
def get_top_comment_karma(amount, hours=None):
    return get_top_karma_type("comment_karma", amount, hours)
    
    
def get_top_gold(amount, hours=None):
    return get_top_karma_type("gold", amount, hours)
    
    
if __name__ == "__main__":
    init()
    