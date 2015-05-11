import json
import unit

UNIT_PATH = "../data/units"
SAVE_PATH = "../data/game"

def load_game():
    with open(SAVE_PATH, 'r') as f:
        data = json.load(f)
    game = Game(data["link_karma"], data["comment_karma"], 
            data["lifetime_link"], data["lifetime_comment"], 
            data["runtime"])
    game.load_units()
    return game

class Game:

    def __init__(self, link_karma, comment_karma, lifetime_link, 
            lifetime_comment, runtime):
        self.link_karma = link_karma
        self.comment_karma = comment_karma
        self.lifetime_link = lifetime_link
        self.lifetime_comment = lifetime_comment
        self.runtime = runtime
        
    def load_units(self):
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
        return self.link_karma
        
    def get_comment_karma(self):
        return self.comment_karma
        
    def get_lifetime_link(self):
        return self.lifetime_link
        
    def get_lifetime_comment(self):
        return self.lifetime_comment
        
    def get_lifetime_total(self):
        return self.get_lifetime_link() + self.get_lifetime_karma()
        
    def add_link_karma(self, user, karma):
        self.link_karma += karma
        self.lifetime_link += karma
        user.add_link_karma(karma)
        
    def add_comment_karma(self, user, karma):
        self.comment_karma += karma
        self.lifetime_comment += karma
        user.add_comment_karma(karma)
        print "ck: %d" % self.comment_karma
        
    def get_unit(self, type, unit_name):
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
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            print ":: no %s unit found for '%s'" % (type, unit_name)
            return False
        print ":: buying %d of %s %s" % (quantity, type, unit.name)
        return unit.buy(self, reddit, type, user, quantity)
        
    def post(self, reddit, type, user, unit_name):
        unit = self.get_unit(type, unit_name)
        if unit is None: 
            print ":: no %s unit found for '%s'" % (type, unit_name)
            return False
        print ":: posting %s %s" % (unit.name, type)
        return unit.post(self, reddit, type, user)
        
    def parse_command(self, user, command, reddit):
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
            #reddit
        
    def save(self):
        try:
            with open(SAVE_PATH, 'w') as f:
                json.dump({"karma":karma, "lifetime_karma":lifetime_karma,
                        "runtime":runtime}, f)
            return True
        except:
            traceback.print_exc()
            return False