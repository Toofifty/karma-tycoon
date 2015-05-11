#!/user/bin/env pthon
"""
Karma Tycoon Bot
Texter class
texter.py

http://karma.matho.me/
"""

import re, random
TEXT_PATH = "../data/text/"

class Texter:
    """Texter text class
    
    Used to import text and populate
    it with data for Reddit Markdown.    
    """
    
    def choose_alts(self, text):
        """Finds alt lists, chooses 1 alt and replaces
        
        return string text with all alts chosen
        """
        
        alt_pattern = re.compile(r'{\|(.*)\|}')
        alt_match = re.findall(alt_pattern, text)
        
        i = 0
        
        while True:
            try:
                alts = alt_match[i]
                alt_list = alts.split("|")
                alt = alt_list[random.randint(0, len(alt_list) - 1)]
                text = text.replace("{|" + alts + "|}", alt)
                i += 1
            except IndexError:
                break
        
        return text
        
    def pop_unit_table(self, unit):
        """Populate a unit table
        
        return string Markdown unit table
        """
        
        fn = "unit_table.txt"
        if self.table_template is None:
            with open(TEXT_PATH + fn, 'r') as f:
                self.table_template = f.read()
        
        table = self.table_template
        
        namevar = {
            "short_name": unit.get_short_name(),
            "name": unit.get_name(),
            "cost": unit.get_cost(),
            "cooldown": unit.get_cooldown(),
            "amount": unit.get_amount(),
            "pay": unit.get_profit(),
            "time": unit.get_time()
        }
        
        for k, v in namevar.iteritems():
            table = text.replace("{" + k + "}", v)
            
        return table
        
        
    def pop_units_list(self, units):
        """Creates a list of unit tables as a string
        
        return string tables
        """
        
        tables = ""
        for unit in units:
            tables = tables + "\n" + pop_unit_table(unit)
            
        return tables
        
    def pop_op(self, game, hs, history):
        """Populate the OP
        
        return string Markdown OP text
        """
    
        fn = "op.txt"
        with open(TEXT_PATH + fn, 'r') as f:
            text = f.read()
        
        namevar = {
            "last_op_update": None,
            "link_karma": game.get_link_karma(),
            "comment_karma": game.get_comment_karma(),
            "gold": game.get_gold(),
            "top_link_all": hs.get_top_link_all(),
            "top_comment_all": hs.get_top_comment_all(),
            "top_g_all": hs.get_top_g_all(),
            "top_link_24h": hs.get_top_link_24h(),
            "top_comment_24h": hs.get_top_comment_24h(),
            "top_g_24h": hs.get_top_g_24h(),
            "last_hs_update": hs.get_last_hs_update(),
            "comment_units": pop_units_list(game.get_comment_units()),
            "link_units": pop_units_list(game.get_link_units())
        }
        
        for k, v in namevar.iteritems():
            text = text.replace("{" + k + "}", v)
            
        return text        
        
        
    def pop_hs(self):
        pass
        
    def pop_fail(self, reason):
        """Populates the command fail message
        
        return string populated text with alts chosen
        """
        fn = "fail_cmd.txt"
        with open(TEXT_PATH + fn, 'r') as f:
            text = f.read()
        
        text = text.replace("{reason}", reason)
        text = self.choose_alts(text)
        
        return text
        
    def pop_success(self, action):
        """Populates the command success message
        
        return string populated text with alts chosen
        """
        
        fn = "success_cmd.txt"
        with open(TEXT_PATH + fn, 'r') as f:
            text = f.read()
            
        text = text.replace("{action}", action)
        text = self.choose_alts(text)
        
        return text
    
    def pop_gilded(self, chance):
        """Populates the command gilded message
        
        return string populated text with alts chosen
        """
        
        fn = "success_cmd_gilded.txt"
        with open(TEXT_PATH + fn, 'r') as f:
            text = f.read()
            
        text = text.replace("{chance}", chance)
        text = self.choose_alts(text)
        
        return text
