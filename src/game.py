import json

UNIT_PATH = "../data/units"
SAVE_PATH = "../data/game"

def load_game():
    with open(SAVE_PATH) as f:
        data = json.load(f)
    game = Game(data["karma"], data["lifetime_karma"], data["runtime"])
    game.load_units()

class Game:

    def __init__(self, karma, lifetime_karma, runtime):
        self.karma = karma
        self.lifetime_karma = lifetime_karma
        self.runtime = runtime
        
    def load_units(self):
        self.units = []
        
    def get_karma(self):
        return karma
        
    def add_karma(self, user, karma):
        self.karma += karma
        user.add_karma(karma)
        
    def buy_unit(self, user, unit_name, quantity=1):
        unit = get_unit(unit_name)
        if unit is None: 
            return False
        return unit.buy(user, quantity)
        
    def get_unit(self, unit_name):
        for unit in units:
            if (unit.name is unit_name or unit.short_name is unit_name):
                return unit
        return None
        
    def post(self, user, unit_name):
        unit = get_unit(unit_name)
        if unit is None: 
            return False
        
    def parse_command(self, command):
        pass
        
    def save(self):
        try:
            with open(SAVE_PATH, 'w') as f:
                json.dump({"karma" = karma, "lifetime_karma" = lifetime_karma,
                        "runtime" = runtime}, f)
            return True
        except:
            traceback.print_exc()
            return False