#!/user/bin/env pthon
"""
Karma Tycoon Bot
User class
user.py

http://karma.matho.me/
"""

import db

USERS = []

def get_user(name):
    """Get User object from users list

    return user object or None
    """
    for user in USERS:
        if user.name == name:
            return user
    return User(name)


class User(object):
    """User class

    Stores information about a user, tied to their
    Reddit username
    """

    def __init__(self, username):
        """Initialise user

        Create save file if none exists,
        load from save.
        """

        self.name = username
        self.load_data(username)
        USERS.append(self)
        print ":: loaded user %s" % self.name


    def get_flair(self):
        """Get flair to use on Reddit

        Examples:
            (most karma, 12 gold)
            1st 3000 LK | 4000 CK 12x

            (low karma, no gold)
            20 LK | 30 CK

            (high karma, 1 gold)
            19th 1000LK | 2140 CK 1x

        return str flair text
        """

        flair = ""
        pos = db.get_position(self)

        if pos <= 20:
            flair = str(pos) + ("st" if pos == 1 else ("nd" if pos == 2 else \
                    ("rd" if pos == 3 else ""))) + " | "

        flair = flair + "%d LK | %d CK" % (self.link_karma, self.comment_karma)

        if self.gold >= 1:
            flair = "x" + str(self.gold) + " " + flair

        return flair


    def get_flair_css(self):
        """Get flair css class(es) to use on Reddit

        Appends modifiers to css text

        More modifiers may be added later.

        return str css class(es) (sep by space)
        """

        css = ""
        pos = db.get_position(self)

        if pos == 1:
            css = "first"

        elif pos == 2:
            css = "second"

        elif pos == 3:
            css = "third"

        elif pos <= 20:
            css = "top20"

        elif self.gold >= 1:
            css = "gold"

        return css


    def get_link_karma(self):
        """Get amount of link karma"""

        return self.link_karma


    def get_comment_karma(self):
        """Get amount of comment karma"""

        return self.comment_karma


    def get_total_karma(self):
        """Get link karma + comment karma"""

        return self.comment_karma + self.link_karma


    def load_data(self, name):
        """Load data in from db"""

        data = db.get_user(name)
        self.title = data["title"]
        self.gold = data["gold"]
        self.link_karma = data["link_karma"]
        self.comment_karma = data["comment_karma"]


    def save_data(self):
        """Save data to db"""

        db.update_user(self)


    def add_link_karma(self, karma):
        """Add to link karma"""

        self.link_karma += karma


    def add_comment_karma(self, karma):
        """Add to comment karma"""

        self.comment_karma += karma


    def add_gold(self):
        """Add to gold"""

        self.gold += 1
