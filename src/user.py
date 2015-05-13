#!/user/bin/env pthon
"""
Karma Tycoon Bot
User class
user.py

http://karma.matho.me/
"""

import json, os

USER_PATH = "../data/user/"
EXT = ".kt"

users = []

def get_user(name):
    """Get User object from users list
    
    return user object or None
    """
    for user in users:
        if user.name is name:
            return user
    return None

class User:
    """User class
    
    Stores information about a user, tied to their
    Reddit username
    """

    def __init__(self, username):
        """Initialise user
        
        Create save file if none exists,
        load from save.
        """
    
        self.name = name
        if not os.path.exists(USER_PATH + self.name + EXT):
            self.create_file()
        self.load_data(name)
            
            
    def get_flair(self, stats):
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
        pos = stats.get_position(self)
        
        if pos <= 20:
            flair = str(pos) + ("st" if pos == 1 else ("nd" if pos == 2 else \
                    ("rd" if pos == 3 else ""))) + " | "
                    
        flair = flair + "%d LK | %d CK" % (self.link_karma, self.comment_karma)
                    
        if self.gold >= 1:
            flair = "flair" + " " + str(self.gold) + "x"
            
        return flair
        
        
    def get_flair_css(self, stats):
        """Get flair css class(es) to use on Reddit
        
        Appends modifiers to css text
        
        More modifiers may be added later.
        
        return str css class(es) (sep by space)
        """
    
        class = ""
            
        pos = stats.get_position(self)
        
        if pos == 1:
            class = "first"
            
        elif pos == 2:
            class = "second"
            
        elif pos == 3:
            class = "third"
            
        elif pos <= 20:
            class = "top20"
            
        elif self.gold >= 1:
            class = "gold"
            
        return class
        
        
    def create_file(self):
        """Create a file with empty/0 values"""
        
        with open(USER_PATH + self.name + EXT, 'w') as f:
            json.dump({"title":"", "gold":0, "link_karma":0, 
                    "comment_karma":0, "commands":0, "purchases":{}}, f)
        
        
    def load_data(self, name):
        """Load data in from json"""
        
        try:
            with open(USER_PATH + name + EXT, 'r') as f:
                self.data = json.load(f)
            self.title = self.data["title"]
            self.gold = self.data["gold"]
            self.link_karma = self.data["link_karma"]
            self.comment_karma = self.data["comment_karma"]
            self.purchases = self.data["purchases"]
            self.commands = self.data["commands"]
        except ValueError:
            self.create_file()
            self.load_data(name)
        
        
    def jason(self):
        """Convert volatile attributes to json
        
        return json statham
        """
        
        statham = {}
        for key in self.data:
            statham[key] = getattr(self, key)
        return statham
        
        
    def save_data(self):
        """Save data to user file"""
    
        with open(USER_PATH + self.name + EXT, 'w') as f:
            json.dump(self.jason(), f)
    
    
    def add_purchase(self, id, quantity):
        """Adds _quantity_ purchased to dict if key _id_
        exists, else creates key _id_
        
        """
    
        try:
            self.purchases[id] += quantity
        except KeyError:
            self.purchases[id] = quantity
        
        
    def add_link_karma(self, karma):
        """Add to link karma"""
    
        self.link_karma += karma
        
        
    def add_comment_karma(self, karma):
        """Add to comment karma"""
    
        self.comment_karma += karma
        
        
    def add_gold(self):
        """Add to gold"""
    
        self.gold += 1
