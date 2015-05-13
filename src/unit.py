#!/user/bin/env pthon
"""
Karma Tycoon Bot
Unit class
unit.py

http://karma.matho.me/
"""

from datetime import datetime, timedelta

# multiplier to buy price after a purchase
cost_mult = 1.3

def from_dict(id, dict, type):
    """Translate a dictionary into a Unit object
    with id
    
    Units are stored as follows (inside a list):
    "comment": [
        {
            "amount": 0,
            "id": "C01",
            "init_cost": 30,
            "init_profit": 7,
            "init_time": 16,
            "name": "Unpopular opinion",
            "short_name": "unpop"
        },
        ...
    ],
    "link": [
        {
            "amount": 0,
            "id": "L22",
            "init_cost": 575000,
            "init_profit": 7779,
            "init_time": 345600,
            "name": "Top of /r/all",
            "short_name": "r-all"
        },
        ...
    ]
        
    returns Unit object
    """
    
    return Unit(type, id, dict["name"], dict["short_name"],
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
        
    
    def get_short_name(self):
        return self.short_name
    
    
    def get_name(self):
        return self.name
        
        
    def get_amount(self):
        return self.amount
        
        
    def get_time(self):
        """Get total cooldown time
        
        In future will be multiplied by a speed mult here.
        """
        return self.convert_from_seconds(self.init_time * 1)
        
        
    def get_suffix(self):
        """Get type of karma as suffix
        
        return str comment ? 'ck', link ? 'lk'
        """
        return self.type[0] + "k"
        
        
    def get_profit(self):
        """Get the karma profit
        
        return int init_profit * amount
        """
        
        return int(self.init_profit * self.amount)
        
        
    def get_next_profit(self):
        """Get the karma profit of next unit
        
        return int init_profit * (amount + 1)
        """
        
        return int(self.init_profit * (self.amount + 1))
        
        
    def get_cost(self, quantity=1):
        """Get the karma cost of purchasing _quantity_ units
        
        TODO - add calculations for != 1 quantities.
        
        return int init_cost * cost_mult^amount
        """
        
        return int(self.init_cost * cost_mult ** self.amount)
        
        
    def buy(self, game, history, type, user, quantity=1):
        """Buy _quantity_ units
        
        Checks if enough of _type_ karma is available
        and purchases _quantity_ units.
        
        Purchase info is then added to the user and
        karma is deducted.
        
        return true if successful
        """
        
        cost = self.get_cost(quantity)
        
        if type == "comment" and game.get_comment_karma() >= cost:
        
            self.amount += quantity
            user.add_purchase(self.id, quantity)
            history.add_purchase(user, type, self, quantity)
            game.comment_karma -= cost
            
        elif type == "link" and game.get_link_karma() >= cost:      
        
            self.amount += quantity
            user.add_purchase(self.id, quantity)
            history.add_purchase(user, type, self, quantity)
            game.link_karma -= cost
            
        else:         
            return False, "Buy failed, not enough %s karma." % type
            
        return True, "Bought %dx **%s** for **%d** %s karma." \
                % (quantity, self.name, cost, type)
        
        
    def post(self, game, history, type, user):
        """ "Post" this comment / link
        
        Adds get_profit to game karma (and use karma)
        
        return true if successful
        """
        
        if self.check_cooldown():
        
            karma = self.get_profit()
        
            if type == "comment":
                game.add_comment_karma(user, karma)
                
            elif type == "link":
                game.add_link_karma(user, karma)
                
            
            if game.random_gold(user, karma):
                history.add_post(user, type, unit, karma, True)
                return True, str(karma / 10000), True
                
            else:
                history.add_post(user, type, unit, karma, False)
                return True, "Gained **%d** %s karma." % (karma, type), False
                
        return False, "**%s** is still in cooldown. **%s** remaining." \
                % (self.name, self.get_cooldown()), False
        
        
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

    
    def get_cooldown(self):
        return self.convert_from_seconds(self.cooldown)
        
        
    def convert_from_seconds(self, secs):
        """Convert the given seconds into X days, 
        X hours, X minutes, X seconds string.
        
        Does not add 'X days' if X == 0, etc.
        """
        
        sec = timedelta(seconds=secs)
        d = datetime(1, 1, 1) + sec        
        text = ""
        
        if d.day - 1 > 0:
            text = text + str(d.day - 1) + " day" + ("s " if not d.day - 1 == 1 else " ")
        if d.hour > 0:
            text = text + str(d.hour) + " hour" + ("s " if not d.hour == 1 else " ")
        if d.minute > 0:
            text = text + str(d.minute) + " minute" + ("s " if not d.minute == 1 else " ")
        if text == "":
            text = text + str(d.second) + " second" + ("s" if not d.second == 1 else "")
            
        if text.endswith(" "):
            text = text[:-1]
            
        return text
        