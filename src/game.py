#!/user/bin/env pthon
"""
Karma Tycoon Bot
Game controller class
game.py

http://karma.matho.me/
"""

import json, random, os, sys
import unit, texter

DATA_PATH = "../data/"
UNIT_FILE = DATA_PATH + "units.kt"
GAME_FILE = DATA_PATH + "game.kt"

class Game:
    """Game object
    
    Handles karma points, command parsing,
    and actions.
    
    The game is stored as follows:
    {
        "gold": 0,
        "link_karma": 0,
        "comment_karma": 0,
        "lifetime_link": 0,
        "lifetime_comment": 0,
        "runtime": 0
    }
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
        
        if not os.path.exists(GAME_FILE):
            print ":: no game save found, create new? (y/n)"
            if raw_input().lower() in ["y","yes"]:
                self.new_game()
                print ":: game save created."
            else:
                print ":: please resolve the error manually."
                print ":: exiting..."
                sys.exit()

        with open(GAME_FILE, 'r') as f:
            self.data = json.load(f)
            
        self.gold = self.data["gold"]
        self.link_karma = self.data["link_karma"]
        self.comment_karma = self.data["comment_karma"]
        self.lifetime_link = self.data["lifetime_link"]
        self.lifetime_comment = self.data["lifetime_comment"]
        self.runtime = self.data["runtime"]
        self.load_units();
        self.texter = texter.Texter()
        
        
    def new_game(self):
        """Creates a new game file
        
        RESETS CURRENT SAVE
        
        Only to be used if current save 
        isn't found.
        """
        
        with open(GAME_FILE, 'w') as f:
            json.dump({
                "gold": 0,
                "link_karma": 0,
                "comment_karma": 0,
                "lifetime_link": 0,
                "lifetime_comment": 0,
                "runtime": 0
            }, f)
        
        
    def load_units(self):
        """Load units into link_units and comment_units
        
        Creates units from data found in UNIT_PATH
        """
        
        self.link_units = []
        self.comment_units = []
        
        with open(UNIT_FILE, 'r') as f:
            data = json.load(f)
            
        i = 0
        for d in data["comment"]:
            self.comment_units.insert(i, unit.from_dict(i, d, "comment"))
            i += 1
        #for id, attrs in data["link"]:
        #    self.comment_units[int(id)] = unit.from_dict(id, attrs)
        
        
    def get_gold(self):
        """return gold points"""
        
        return self.gold
        
        
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
        self.lifetime_link += karma
        user.add_link_karma(karma)
        return True
        
        
    def add_comment_karma(self, user, karma):
        """Add comment karma to tally and user's tally"""
        
        self.comment_karma += karma
        self.lifetime_comment += karma
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
        
        
    def buy_unit(self, history, type, user, unit_name, quantity=1):
        """Buy _quantity_ units in _type_ 
        
        return true if unit.buy(), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            return False, "Unit name **%s** not recognised." % unit_name
            
        return unit.buy(self, history, type, user, quantity)
        
        
    def post(self, history, type, user, unit_name):
        """ "Post" a comment / link
        
        return true if unit.post9), false if unit not found
        """
        
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            return False, "Unit name **%s** not recognised." % unit_name, False
            
        return unit.post(self, history, type, user)
        
        
    def parse_command(self, user, command, history):
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
                success, info = self.buy_unit(history, "comment", user, " ".join(args[2:]))
                
            elif args[1] in ["link","l"]:
                success, info = self.buy_unit(history, "link", user, " ".join(args[2:]))
                
        elif args[0] in ["post","p"] and len(args) >= 3:
        
            if args[1] in ["comment","c"]:
                success, info, gold = self.post(history, "comment", user, " ".join(args[2:]))
                
            elif args[1] in ["link","l"]:
                success, info, gold = self.post(history, "link", user, " ".join(args[2:]))
            
        # try and give a detailed error explanation
        else:
        
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
                
        if not success:
            print("bad command by " + user.username)
            
        return success, info, gold
        
        
    def jason(self):
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
        
        with open(GAME_FILE, 'w') as f:
            json.dump(self.jason(), f)
