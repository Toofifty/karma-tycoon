import json, os

USER_PATH = "../data/user/"
EXT = ".kt"

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
    
        self.username = username
        if not os.path.exists(USER_PATH + self.username + EXT):
            self.create_file()
        self.load_data(username)
            
            
    def get_flair(self):
        """return str flair for use on Reddit"""
        
        return "L: %d C: %d" % (self.link_karma, self.comment_karma)
        
    def create_file(self):
        """Create a file with empty/0 values"""
        
        with open(USER_PATH + self.username + EXT, 'w') as f:
            json.dump({"title":"", "gold":0, "link_karma":0, 
                    "comment_karma":0, "purchases":{}}, f)
        
        
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
    
        with open(USER_PATH + self.username + EXT, 'w') as f:
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
