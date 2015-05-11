cost_mult = 1.3

def from_dict(id, dict):
    u = Unit(dict["type"], id, dict["name"], dict["short_name"],
            dict["init_cost"], dict["init_profit"], dict["init_time"],
            dict["amount"])
    return u
            
class Unit:
    
    cooldown = 0
    
    def __init__(self, type, id, name, short_name, init_cost, 
            init_profit, init_time, amount):
        self.type = type
        self.id = id
        self.name = name
        self.short_name = short_name
        self.init_cost = init_cost
        self.init_profit = init_profit
        self.init_time = init_time
        self.amount = amount
        
    def is_named(self, name):
        return name == self.name or name == self.short_name
        
    def get_profit(self):
        return int(self.init_profit * self.amount)
        
    def get_cost(self, quantity=1):
        return int(self.init_cost * cost_mult ** self.amount)
        
    def buy(self, game, reddit, type, user, quantity=1):
        print type, game.get_comment_karma(), self.get_cost(quantity)
        if type == "comment" and game.get_comment_karma() >= self.get_cost(quantity):
            self.amount += quantity
            user.add_purchase(self.name, quantity)
            game.comment_karma -= self.get_cost(quantity)
            print ":: bought comment, total %s %d" % (self.short_name, self.amount)
            return True
        elif game.get_link_karma() >= self.get_cost(quantity):
            self.amount += quantity
            user.add_purchase(self.name, quantity)
            game.link_karma -= self.get_cost(quantity)
            print ":: bought link, total %s %d" % (self.short_name, self.amount)
            return True
        print ":: buy failed"
        return False
        
    def post(self, game, reddit, type, user):
        if self.check_cooldown():
            if type == "comment":
                game.add_comment_karma(user, self.get_profit())
                return True
            elif type == "link":
                game.add_link_karma(user, self.get_profit())
                return True
        return False
        
    def reset_cooldown(self):
        self.cooldown = init_time
        
    def check_cooldown(self):
        if (self.cooldown <= 0):
            self.cooldown = 0
            return True
        return False     
    
    def update_cooldown(self, dt):
        self.cooldown -= dt
