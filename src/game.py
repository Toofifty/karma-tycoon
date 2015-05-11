#!/user/bin/env pthon
"""
Karma Tycoon Bot
Game class
game.py

http://karma.matho.me/
"""

import json
import unit

UNIT_PATH = "../data/units"
SAVE_PATH = "../data/game"

class Game:
    """Game object
    
    Handles karma points, command parsing,
    and actions.
    """

    def __init__(self):
        """Create game object from data in SAVE_PATH
        
        JSON file must have keys:
            "gold" int
            "link_karma" int
            "comment_karma" int
            "lifetime_link" int
            "lifetime_comment" int
            "runtime" int
        """
        
        with open(SAVE_PATH, 'r') as f:
            self.data = json.load(f)
            
        self.gold = self.data["gold"]
        self.link_karma = self.data["link_karma"]
        self.comment_karma = self.data["comment_karma"]
        self.lifetime_link = self.data["lifetime_link"]
        self.lifetime_comment = self.data["lifetime_comment"]
        self.runtime = data["runtime"]
        self.load_units();
        
        
    def load_units(self):
        """Load units into link_units and comment_units
        
        Creates units from data found in UNIT_PATH
        """
        
        self.link_units = []
        self.comment_units = []
        
        with open(UNIT_PATH, 'r') as f:
            data = json.load(f)
            
        for id in data["comment"]:
            i = int(id) - 1
            self.comment_units.append(unit.from_dict(i, data["comment"][id]))
        #for id, attrs in data["link"]:
        #    self.comment_units[int(id)] = unit.from_dict(id, attrs)
        
        
    def get_link_karma(self):
        """return link karma points"""
        
        return self.link_karma
        
        
    def get_comment_karma(self):
        """return comment karma points"""
        
        return self.comment_karma
        
        
    def get_lifetime_link(self):
        """return lifetime total link karma points"""
        
        return self.lifetime_link
        
        
    def get_lifetime_comment(self):
        """return lifetime total comment karma points"""
        
        return self.lifetime_comment
        
        
    def get_lifetime_total(self):
        """return lifetime total karma points"""
        
        return self.get_lifetime_link() + self.get_lifetime_karma()
        
        
    def add_link_karma(self, user, karma):
        """Add link karma to tally and user's tally"""
        
        self.link_karma += karma
        self.lifetime_link += karma
        user.add_link_karma(karma)
        print "lk: %d" % self.link_karma
        
    def add_comment_karma(self, user, karma):
        """Add comment karma to tally and user's tally"""
        
        self.comment_karma += karma
        self.lifetime_comment += karma
        user.add_comment_karma(karma)
        print "ck: %d" % self.comment_karma
        
    def get_unit(self, type, unit_name):
        """Get unit from name and type
        
        return Unit object or None
        """
    
        if type is "comment":
        
            for unit in self.comment_units:
                if unit.is_named(unit_name):
                    return unit
                    
        elif type is "link":
        
            for unit in self.link_units:
                if unit.is_named(unit_name):
                    return unit
                    
        return None
        
        
    def buy_unit(self, reddit, type, user, unit_name, quantity=1):
        """Buy _quantity_ units in _type_ 
        
        return true if unit.buy(), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            print ":: no %s unit found for '%s'" % (type, unit_name)
            return False
            
        print ":: buying %d of %s %s" % (quantity, type, unit.name)
        return unit.buy(self, reddit, type, user, quantity)
        
        
    def post(self, reddit, type, user, unit_name):
        """ "Post" a comment / link
        
        return true if unit.post9), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            print ":: no %s unit found for '%s'" % (type, unit_name)
            return False
            
        print ":: posting %s %s" % (unit.name, type)
        return unit.post(self, reddit, type, user)
        
        
    def parse_command(self, user, command, reddit):
        """Parse a user comment (str)
        
        Accepts either full word or first letter of
        command.
        
        Commands:
            buy [comment|link] [unit.name|unit.short_name] (quantity)
            b [c|l] [unit.name|unit.short_name] (quantity)
            
            post [comment|link] [unit.name|unit.short_name]
            p [c|l] [unit.name|unit.short_name]
            
            buy-gold [comment|link] [unit.name|unit.short_name]
            bg [c|l] [unit.name|unit.short_name]
        
        return true if successful
        """
    
        successful = False
        args = command.split(" ")
        if args[0] in ["buy","b"] and len(args) >= 4:
        
            if args[1] in ["comment","c"]:
                self.buy_unit(reddit, "comment", user, " ".join(args[2:-1]))
                successful = True
                
            elif args[1] in ["link","l"]:
                self.buy_unit(reddit, "link", user, " ".join(args[2:-1]))
                successful = True
                
        elif args[0] in ["post","p"] and len(args) >= 3:
        
            if args[1] in ["comment","c"]:
                self.post(reddit, "comment", user, " ".join(args[2:]))
                successful = True
                
            elif args[1] in ["link","l"]:
                self.post(reddit, "link", user, " ".join(args[2:]))
                successful = True
                
        if not successful:
            print("bad command")
            # post reddit
            
        return successful
        
        
    def json(self):
        """Convert volatile attributes to json
        
        return json bateman
        """
        bateman = {}
        for key in self.data:
            bateman[key] = getattr(self, key)
        return bateman
        
        
    def save(self):
        """Save current data to file
        
        return true if successful
        """
        
        with open(SAVE_PATH, 'w') as f:
            json.dump(self.json(), f)
