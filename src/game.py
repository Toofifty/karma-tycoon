#!/user/bin/env pthon
"""
Karma Tycoon Bot
Game controller class
game.py

http://karma.matho.me/
"""

import json, random, os, sys, time
import unit, texter, db, unit

class Game:
    """Game object
    
    Handles karma points, command parsing,
    and actions.
    """
    
    def __init__(self):
        """Create game object from data in db"""
        
        self.load_data(db.get_game())
        self.comment_units = self.load_units("comment")
        self.link_units = self.load_units("link")
        self.texter = texter.Texter()
        
        
    def load_data(self, data):
        """Loads attributes from data dict"""
        
        self.gold = data["gold"]
        self.link_karma = data["link_karma"]
        self.comment_karma = data["comment_karma"]
        self.lifetime_lk = data["lifetime_lk"]
        self.lifetime_ck = data["lifetime_ck"]
        self.runtime = data["runtime"]
        self.session_start = time.time()
        
        
    def load_units(self, type):
        """Load units into link_units and comment_units
        
        Creates units from data found in UNIT_PATH
        """
        
        units = []
        
        for unit_data in db.get_units(type):
            units.append(unit.Unit(unit_data))
        
        return units
        
        
    def get_gold(self):
        """return gold points"""
        
        return self.gold
        
        
    def get_karma(self, type):
        if type.lower() == "comment":
            return self.comment_karma
            
        elif type.lower() == "link":
            return self.link_karma
            
            
    def get_lifetime_karma(self, type):
        if type.lower() == "comment":
            return self.lifetime_ck
            
        elif type.lower() == "link":
            return self.lifetime_lk
            
        
    def get_lifetime_total(self):
        """return lifetime total karma points"""
        
        return self.get_lifetime_karma("comment") \
                + self.get_lifetime_karma("link")
        
        
    def random_gold(self, user, karma):
        """Randomly awards gold, dependent on karma gained"""
    
        if random.randint(0, 1000000) < karma:
            self.gold += 1
            user.add_gold()
            return True
        return False
        
        
    def add_link_karma(self, user, karma):
        """Add link karma to tally and user's tally"""
        
        self.link_karma += karma
        self.lifetime_lk += karma
        user.add_link_karma(karma)
        return True
        
        
    def add_comment_karma(self, user, karma):
        """Add comment karma to tally and user's tally"""
        
        self.comment_karma += karma
        self.lifetime_ck += karma
        user.add_comment_karma(karma)
        return True
        
        
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
        
        
    def buy_unit(self, type, user, unit_name, quantity=1):
        """Buy _quantity_ units in _type_ 
        
        return true if unit.buy(), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            return False, "Unit name **%s** not recognised." % unit_name
            
        return unit.buy(self, type, user, quantity)
        
        
    def post(self, type, user, unit_name):
        """ "Post" a comment / link
        
        return true if unit.post9), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            return False, "Unit name **%s** not recognised." % unit_name, False
            
        return unit.post(self, type, user)
        
        
    def parse_command(self, user, command):
        """Parse a user comment (str)
        
        Accepts either full word or first letter of
        command.
        
        Commands:
            buy [comment|link] [unit.name|unit.short_name]
            b [c|l] [unit.name|unit.short_name]
            
            post [comment|link] [unit.name|unit.short_name]
            p [c|l] [unit.name|unit.short_name]
            
            buy-gold [comment|link] [unit.name|unit.short_name]
            bg [c|l] [unit.name|unit.short_name]
            
            
        Specific quantity purchases will come at a later date.
        
        return true if successful
        """
    
        success = False
        gold = False
        args = command.split(" ")
        
        if args[0] in ["buy","b"] and len(args) >= 3:
        
            if args[1] in ["comment","c"]:
                success, info = self.buy_unit("comment", user, " ".join(args[2:]))
                
            elif args[1] in ["link","l"]:
                success, info = self.buy_unit("link", user, " ".join(args[2:]))
                
        elif args[0] in ["post","p"] and len(args) >= 3:
        
            if args[1] in ["comment","c"]:
                success, info, gold = self.post("comment", user, " ".join(args[2:]))
                
            elif args[1] in ["link","l"]:
                success, info, gold = self.post("link", user, " ".join(args[2:]))
            
        else:
            
            return False, "not command", False
            
        # try and give a detailed error explanation        
        if not success:
        
            print("bad command by " + user.name)
            
            if len(args) < 3:
            
                info = "Invalid arguments length."
                
            elif not args[0] in ["post","p","buy","b"]:
            
                info = "The only commands currently supported are \
                        *buy* (or *b*) and *post* (or *p*).\n **%s**  \
                        was not recognised." % args[0]
                        
            elif not args[1] in ["link","l","comment","c"]:
            
                info = "Your post type **%s** was not recognised. \
                        The two types are: *comment* (or *c*) and \
                        *link* (or *l*)." % args[1]
            
        return success, info, gold
        
        
    def save(self):
        """Save current data to file
        
        return true if successful
        """
        
        with open(GAME_FILE, 'w') as f:
            json.dump(self.jason(), f)
