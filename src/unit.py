cost_mult = 1.3

class Unit:
    
    self.amount = 0
    self.cooldown = 0
    
    def __init__(self, id, name, short_name, init_cost, init_profit,
            init_time):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.init_cost = init_cost
        self.init_profit = init_profit
        self.init_time = init_time
        
    def get_profit(self):
        return int(self.profit * self.amount)
        
    def get_cost(self, quantity=1):
        return int(self.cost * cost_mult ** self.amount)
        
    def buy(self, game, user, quantity=1):
        if game.karma >= self.get_cost(quantity):
            self.amount += quantity
            user.add_purchase(id, quantity)
            game.karma -= self.get_cost(quantity)
            return True
        return False
        
    def post(self, game, user):
        if check_cooldown():
            game.add_karma(self.get_profit())
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
