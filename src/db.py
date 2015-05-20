#!/user/bin/env pthon
"""
Karma Tycoon Bot
SQL Database interface functions
db.py

http://karma.matho.me/
"""

import sqlite3, time

CON = sqlite3.connect("../data/kt.db")
CON.row_factory = sqlite3.Row
CUR = CON.cursor()

def init():
    """Create tables"""

    with CON:
        CUR.execute(
            "CREATE TABLE users(name TEXT, title TEXT, gold INT, \
            link_karma INT, comment_karma INT)"

        )

        CUR.execute(
            "CREATE TABLE units(id INTEGER PRIMARY KEY, type TEXT, name TEXT, \
            short TEXT, amount INT, init_cost INT, init_profit INT, \
            init_time INT)"
        )

        CUR.execute(
            "CREATE TABLE commands(id INTEGER PRIMARY KEY, username TEXT, \
            command TEXT, type TEXT, unit_id TEXT, value INT, time_sec INT)"
        )

        CUR.execute(
            "CREATE TABLE game(id INTEGER PRIMARY KEY, gold INT, \
            link_karma INT, comment_karma INT, lifetime_lk INT, \
            lifetime_ck INT, runtime INT)"
        )

        CUR.execute("CREATE TABLE comments(id INT)")


def new_game():
    """Adds a new game record"""

    confirm = raw_input(":: are you sure you wish to reset the game? (y/n)")
    if confirm != "y":
        return

    with CON:
        CUR.execute("SELECT * FROM game")
        games = CUR.fetchall()
        if games is None:
            game_id = 0
        else:
            game_id = len(games)
        CUR.execute("INSERT INTO game VALUES(?, 0, 0, 0, 0, 0, 0)", (game_id,))


def get_game():
    """Get current game info"""

    with CON:
        CUR.execute("SELECT * FROM game ORDER BY id DESC")
        game = CUR.fetchone()
        if game is None:
            print ":: no game save found"
            print ":: creating new..."
            new_game()
            return get_game()

        return game


def update_game(game):
    """Saved the game state"""

    values = (
        game.gold, game.link_karma, game.comment_karma, game.lifetime_lk,
        game.lifetime_ck, game.runtime + time.time() - game.session_start,
        get_game()["id"]
    )

    with CON:
        CUR.execute(
            "UPDATE game SET gold=?, link_karma=?, comment_karma=?, \
            lifetime_lk=?, lifetime_ck=?, runtime=? WHERE id=?", values
        )


def get_users():
    """Gets all the users"""

    with CON:
        CUR.execute("SELECT * FROM users")
        return CUR.fetchall()


def get_user(username):
    """Get the user data for username"""

    with CON:
        CUR.execute("SELECT * FROM users WHERE name=?", (username,))

        user = CUR.fetchone()

        if user is None:
            print ":: creating new user %s" % username
            CUR.execute("INSERT INTO users VALUES(?, '', 0, 0, 0)",
                        (username,))
            return get_user(username)

        return user


def update_user(user):
    """Updates a user record."""

    with CON:
        CUR.execute(
            "UPDATE users SET title=?, gold=?, link_karma=?, comment_karma=? \
            WHERE name=?",
            (user.title, user.gold, user.link_karma, user.comment_karma,
             user.name)
        )


def get_units(unit_type):
    """Retrieve all units of _unit_type_"""

    with CON:
        CUR.execute("SELECT * FROM units WHERE type=?", (unit_type,))
        return CUR.fetchall()


def get_unit(unit_id):
    """Get a unit's data from id"""

    with CON:
        CUR.execute("SELECT * FROM units WHERE id=?", (unit_id,))
        return CUR.fetchall()[0]


def update_unit(unit):
    """Updates a unit (amount, cost, profit)"""

    with CON:
        CUR.execute("UPDATE units SET amount=? WHERE id=?",
                    (unit.amount, unit.id))


def add_command(user, command, unit_type, unit_id, value):
    """Add a player command to the database"""

    with CON:
        CUR.execute(
            "INSERT INTO commands(username, command, type, unit_id, value, \
            time_sec) VALUES(?, ?, ?, ?, ?, ?)",
            (user.name, command, unit_type, unit_id, value, time.time())
        )


def get_command_count(user):
    """List and count commands made by the user"""

    with CON:
        CUR.execute("SELECT * FROM commands WHERE username=?", (user.name,))
        return len(CUR.fetchall())

def add_comment_id(comment_id):
    """Add a comment id to the comments table"""

    with CON:
        CUR.execute("INSERT INTO comments(id) VALUES(?)", (comment_id,))


def has_comment_id(comment_id):
    """Check if comment has already been processed"""

    with CON:
        CUR.execute("SELECT * FROM comments WHERE id=?", (comment_id,))
        return not CUR.fetchone() is None


def get_position(user):
    """Get a user's rank in total karma"""

    with CON:
        CUR.execute(
            "SELECT * FROM users WHERE ? < link_karma + comment_karma",
            (user.get_total_karma(),)
        )
        return len(CUR.fetchall()) + 1


def get_top_karma_type(karma_type, amount, hours=None):
    """Gets _amount_ top users for karma _type_
    in last _hours_ hours.

    If hours is None, gets total karma
    """

    with CON:
        if hours is None:

            CUR.execute("SELECT * FROM users ORDER BY ? DESC", (karma_type,))

            return CUR.fetchall()[:amount]

        else:

            if not karma_type == "gold":
                karma_type = karma_type.replace("_karma", "")

            CUR.execute(
                "SELECT * FROM commands WHERE time_sec > ? AND command=? AND \
                type=?",
                (time.time() - hours * 3600, "post", karma_type)
            )

            commands = CUR.fetchall()

            if len(commands) is 0:
                if type == "gold":
                    return [{"name":"Nobody", karma_type:0}]
                else:
                    return [{"name":"Nobody", karma_type + "_karma":0}]

            tally = {}
            for command in commands:
                if not command["username"] in tally:
                    tally[command["username"]] = command["value"]
                else:
                    tally[command["username"]] += command["value"]

            # sort and place into list
            top_in_hours = []
            for player in sorted(tally, key=tally.get, reverse=True):
                top_in_hours.append({
                    "name":player,
                    karma_type + "_karma":tally[player]
                })

            return top_in_hours[:amount]


def get_top_karma(amount, hours):
    """Get _amount_ of players who have gained the
    most karma over _hours_ hours.
    """

    if hours is None:

        CUR.execute(
            "SELECT * FROM users ORDER BY link_karma + comment_karma DESC"
        )

        return CUR.fetchall()[:amount]

    CUR.execute(
        "SELECT * FROM commands WHERE time_sec > ? AND command=? AND \
        (type=? OR type=?)",
        (time.time() - hours * 3600, "post", "link", "comment")
    )

    commands = CUR.fetchall()

    if len(commands) is 0:
        return [{"name":"Nobody", "karma":0}]

    tally = {}
    tally_link = {}
    tally_comment = {}
    for command in CUR.fetchall():
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
    for player in sorted(tally, key=tally.get, reverse=True):

        top_in_hours.append({
            "name":player,
            "link_karma":tally_link[player],
            "comment_karma":tally_comment[player]
        })

    return top_in_hours[:amount]


def get_top_link_karma(amount, hours=None):
    """Get _amount_ of players who have gained the
    most link karma over _hours_ hours, or of all
    time if hours is None.
    """

    return get_top_karma_type("link_karma", amount, hours)


def get_top_comment_karma(amount, hours=None):
    """Get _amount_ of players who have gained the
    most comment karma over _hours_ hours, or of all
    time if hours is None.
    """
    return get_top_karma_type("comment_karma", amount, hours)


def get_top_gold(amount, hours=None):
    """Get _amount_ of players who have gained the
    most gold over _hours_ hours, or of all
    time if hours is None.
    """
    return get_top_karma_type("gold", amount, hours)


def get_recent_commands(amount):
    """Retrieve _amount_ of previous commands from the database"""

    with CON:
        CUR.execute("SELECT * FROM commands ORDER BY id DESC")
        return CUR.fetchall()[:amount]


# DANGERZONE
# if __name__ == "__main__":
#     init()
