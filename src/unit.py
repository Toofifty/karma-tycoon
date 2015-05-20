#!/user/bin/env pthon
"""
Karma Tycoon Bot
Unit class
unit.py

http://karma.matho.me/
"""

from datetime import datetime, timedelta
import db

# multiplier to buy price after a purchase
COST_MULT = 1.3

class Unit(object):
    """Link / comment unit

    Provides karma when "posted" after a
    cooldown, and can be purchased.
    """

    # timer
    cooldown = 0


    def __init__(self, data):
        """Assign variables that were loaded from db"""

        self.load_data(data)


    def load_data(self, data):
        """Loads attributes from data dict"""

        self.id = data["id"]
        self.type = data["type"]
        self.name = data["name"]
        self.short = data["short"]
        self.amount = data["amount"]
        self.init_cost = data["init_cost"]
        self.init_time = data["init_time"]
        self.init_profit = data["init_profit"]


    def is_named(self, name):
        """Check if this unit is named _name_

        return true if _name_ matches
            this name or short_name
        """

        return name.lower() == self.name.lower() \
                or name.lower() == self.short.lower()


    def get_short(self):
        """Get short name"""

        return self.short


    def get_name(self):
        """Get regular name"""

        return self.name


    def get_amount(self):
        """Get amount of units"""

        return self.amount


    def get_time(self):
        """Get total cooldown time

        In future will be multiplied by a speed mult here.
        """

        return convert_from_seconds(self.init_time * 1)


    def get_cooldown(self):
        """Get current cooldown time left"""

        return convert_from_seconds(self.cooldown)


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

        return int(self.init_cost * COST_MULT ** self.amount)


    def buy(self, game, unit_type, user, quantity=1):
        """Buy _quantity_ units

        Checks if enough of _type_ karma is available
        and purchases _quantity_ units.

        Purchase info is then added to the user and
        karma is deducted.

        return true if successful
        """

        cost = self.get_cost(quantity)

        if unit_type == "comment" and game.get_karma("comment") >= cost:

            game.comment_karma -= cost

        elif unit_type == "link" and game.get_karma("link") >= cost:

            game.link_karma -= cost

        else:
            return False, "Buy failed, not enough %s karma. \
                Cost: %d, %s karma: %d" % (
                    unit_type, cost, unit_type, game.get_karma(unit_type)
                )

        # only reached if purchase is successful
        self.amount += quantity
        db.add_command(user, "buy", type, self.id, quantity)
        db.update_unit(self)

        return True, "Bought %dx **%s** for **%d** %s karma." \
                % (quantity, self.name, cost, type)


    def post(self, game, unit_type, user):
        """ "Post" this comment / link

        Adds get_profit to game karma (and use karma)

        return true if successful
        """

        if self.check_cooldown():

            karma = self.get_profit()

            if unit_type == "comment":
                game.add_comment_karma(user, karma)

            elif unit_type == "link":
                game.add_link_karma(user, karma)

            db.add_command(user, "post", unit_type, self.id, karma)

            if game.random_gold(user, karma):
                db.add_command(user, "post", "gold", self.id, 1)
                return True, str(karma / 10000), True

            else:
                return True, "Gained **%d** %s karma." % (karma, unit_type), False

        return False, "**%s** is still in cooldown. **%s** remaining." \
                % (self.name, self.get_cooldown()), False


    def reset_cooldown(self):
        """Resets the cooldown to max"""

        self.cooldown = self.init_time


    def check_cooldown(self):
        """Checks if cooldown is finished

        return true if cooldown is 0
        """

        if self.cooldown <= 0:
            self.cooldown = 0
            return True
        return False


    def update_cooldown(self, delta):
        """Updates a cooldown.

        Is called after every *actual* comment / command
        if cooldown != 0.
        """

        self.cooldown -= delta


def convert_from_seconds(secs):
    """Convert the given seconds into X days,
    X hours, X minutes, X seconds string.

    Does not add 'X days' if X == 0, etc.
    """

    sec = timedelta(seconds=secs)
    date = datetime(1, 1, 1) + sec
    text = ""

    if date.day - 1 > 0:
        text = text + str(date.day - 1) \
                + " day" + ("s " if not date.day - 1 == 1 else " ")
    if date.hour > 0:
        text = text + str(date.hour) \
                + " hour" + ("s " if not date.hour == 1 else " ")
    if date.minute > 0:
        text = text + str(date.minute) \
                + " minute" + ("s " if not date.minute == 1 else " ")
    if text == "":
        text = text + str(date.second) \
                + " second" + ("s" if not date.second == 1 else "")

    if text.endswith(" "):
        text = text[:-1]

    return text
