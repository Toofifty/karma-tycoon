#!/user/bin/env pthon
"""
Karma Tycoon Bot
History tracker class
history.py

http://karma.matho.me/
"""

HIST_PATH = "../data/hist"

class History:
    """History class
    
    Keeps track of post, buy and upgrade
    history for use in the OP and stats pages.
    
    Actions are stored as follows (inside of a list):
    {
        "action": "buy",
        "type": "comment",
        "unit-id": "c01"
        "user-name": "Toofifty",
        "quantity": 1,
        "time": 12345678,
    },
    {
        "action": "post",
        "type": "link",
        "unit-id": "c02"
        "user-name": "Toofifty",
        "time": 12345679,
    }
    """
    
    def __init__(self):
        pass
        
        
    def add_purchase(self, user, type, unit, quantity):
        pass
        
        
    def add_post(self, user, type, unit, karma, gold):
        pass
        
        
    def save_history(self):
        pass
        
        
    def load_history(self):
        pass
        
        
    def get_recent(self, amount):
        """Get _amount_ past actions, place into
        list of dictionaries.
        
        return list of dictionaries
        """
        
        pass
        