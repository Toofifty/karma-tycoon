import json, os

USER_PATH = "../data/user/"

class User:
    def __init__(self, username):
        self.username = username
        if not os.path.exists(USER_PATH + self.username):
            self.create_file()
        self.load_data(username)
            
    def get_flair(self):
        return "L: %d C: %d" % (self.link_karma, self.comment_karma)
        
    def create_file(self):
        with open(USER_PATH + self.username, 'w') as f:
            f.write('{"title":"", "link_karma":0, "comment_karma":0, "purchases":{}}')
        
    def load_data(self, name):
        with open(USER_PATH + name, 'r') as f:
            self.data = json.load(f)
        self.title = self.data["title"]
        self.link_karma = self.data["link_karma"]
        self.comment_karma = self.data["comment_karma"]
        self.purchases = self.data["purchases"]
        
    def attr_to_json(self):
        data = {}
        for key in self.data:
            data[key] = getattr(self, key)
        return data
        
    def save_data(self):
        with open(USER_PATH + self.username, 'w') as f:
            json.dump(attr_to_json(), f)
    
    def add_purchase(self, id, quantity):
        try:
            self.purchases[id] += quantity
        except KeyError:
            self.purchases[id] = quantity
        
    def add_link_karma(self, karma):
        self.link_karma += karma
        
    def add_comment_karma(self, karma):
        self.comment_karma += karma