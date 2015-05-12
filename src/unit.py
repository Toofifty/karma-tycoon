#!/user/bin/env pthon
"""
Karma Tycoon Bot
Unit class
unit.py

http://karma.matho.me/
"""

# multiplier to buy price after a purchase
cost_mult = 1.3

def from_dict(id, dict):
    """Translate a dictionary into a Unit object
    with id
    
    dictionary must have keys:
        "type" str
        "name" str
        "short_name" str
        "init_cost" int
        "init_profit" int
        "init_time" int
        "amount" int
        
    returns Unit object
    """
    
    return Unit(dict["type"], id, dict["name"], dict["short_name"],
            dict["init_cost"], dict["init_profit"], dict["init_time"],
            dict["amount"])
            
            
class Unit:
    """Link / comment unit
    
    Provides karma when "posted" after a
    cooldown, and can be purchased.
    """
    
    # timer
    cooldown = 0
    
    
    def __init__(self, type, id, name, short_name, init_cost, 
            init_profit, init_time, amount):
        """Assign variables that were loaded from json"""
        
        self.type = type
        self.id = id
        self.name = name
        self.short_name = short_name
        self.init_cost = init_cost
        self.init_profit = init_profit
        self.init_time = init_time
        self.amount = amount
        
        
    def is_named(self, name):
        """Check if this unit is named _name_
        
        return true if _name_ matches 
            this name or short_name
        """
        return name == self.name or name == self.short_name
        
        
    def get_profit(self):
        """Get the karma profit
        
        return int init_profit * amount
        """
        
        return int(self.init_profit * self.amount)
        
        
    def get_cost(self, quantity=1):
        """Get the karma cost of purchasing _quantity_ units
        
        TODO - add calculations for != 1 quantities.
        
        return int init_cost * cost_mult^amount
        """
        
        return int(self.init_cost * cost_mult ** self.amount)
        
    def buy(self, game, reddit, type, user, quantity=1):
        """Buy _quantity_ units
        
        Checks if enough of _type_ karma is available
        and purchases _quantity_ units.
        
        Purchase info is then added to the user and
        karma is deducted.
        
        return true if successful
        """
        
        if type == "comment" and \
                game.get_comment_karma() >= self.get_cost(quantity):
                
            self.amount += quantity
            user.add_purchase(self.name, quantity)
            game.comment_karma -= self.get_cost(quantity)
            print ":: bought comment, total %s %d" % (self.short_name, self.amount)
            return True
            
        elif type == "link" and \
                game.get_link_karma() >= self.get_cost(quantity):
                
            self.amount += quantity
            user.add_purchase(self.name, quantity)
            game.link_karma -= self.get_cost(quantity)
            print ":: bought link, total %s %d" % (self.short_name, self.amount)
            return True
            
        print ":: buy failed, not enough funds"
        return False
        
        
    def post(self, game, reddit, type, user):
        """ "Post" this comment / link
        
        Adds get_profit to game karma (and use karma)
        
        return true if successful
        """
        
        if self.check_cooldown():
        
            if type == "comment":
                game.add_comment_karma(user, self.get_profit())
                return True
                
            elif type == "link":
                game.add_link_karma(user, self.get_profit())
                return True
                
        return False
        
        
    def reset_cooldown(self):
        """Resets the cooldown to max"""
        
        self.cooldown = init_time
        
        
    def check_cooldown(self):
        """Checks if cooldown is finished
        
        return true if cooldown is 0
        """
        if (self.cooldown <= 0):
            self.cooldown = 0
            return True
        return False     
    
    
    def update_cooldown(self, dt):
        """Updates a cooldown.
        
        Is called after every *actual* comment / command
        if cooldown != 0.
        """
        self.cooldown -= dt
