#!/user/bin/env pthon
"""
Karma Tycoon Bot
Text generator class
texter.py

http://karma.matho.me/
"""

import re, random, time
import db

DATA_PATH = "../data/"
TEXT_PATH = DATA_PATH + "text/"

def choose_alts(text):
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


def pop_unit_table(unit, table):
    """Populate a unit table

    return string Markdown unit table
    """

    if unit.check_cooldown():
        cooldown = "[Ready!](/unit_ready)"
    else:
        cooldown = str(unit.get_cooldown()) + " left"

    namevar = {
        "short_name": unit.get_short(),
        "name": unit.get_name(),
        "cost": "-" + str(unit.get_cost()) + " "  + unit.get_suffix(),
        "cooldown": cooldown,
        "amount": str(unit.get_amount()) + "x",
        "pay": "+" + str(unit.get_next_profit()) + " " + unit.get_suffix(),
        "time": "Cooldown: " + str(unit.get_time())
    }

    for ref, value in namevar.iteritems():
        table = table.replace("{" + ref + "}", str(value))

    return table


def pop_units_list(units, game):
    """Creates a list of unit tables as a string

    return string tables
    """

    with open(TEXT_PATH + "unit_table.txt", 'r') as ut_file:
        template = ut_file.read().split("\n")

    tables = "\n".join(template[:-1])
    for i in range(len(units)):
        if units[i].get_cost() < game.get_lifetime_karma(units[i].type) * 2:
            tables = tables + "\n" \
                    + pop_unit_table(units[i], template[-1])

    return tables


def pop_recents_action(data):
    """Populate a single action for a command row"""

    if data["command"] == "post":
        if data["type"] == "gold":
            return "**Received gold!**"
        else:
            return "Posted *%s* for **%d** %s karma" % (
                db.get_unit(data["unit_id"])["name"], data["value"],
                data["type"]
            )
    else:
        return "Bought *%s* for **%d** %s karma" % (
            db.get_unit(data["unit_id"])["name"], data["value"], data["type"]
        )


def pop_recents_row(data, table):
    """Populate a recent commands row

    return string Markdown commands row
    """

    namevar = {
        "user": data["username"],
        "action": pop_recents_action(data),
        "time": time.strftime(
            "%d-%m-%y %I:%M:%S%p",
            time.gmtime(data["time_sec"])
        )
    }

    for ref, value in namevar.iteritems():
        table = table.replace("{" + ref + "}", str(value))

    return table

def pop_recents_list():
    """Creates a list of recent commands tables as a string

    return string tables
    """

    with open(TEXT_PATH + "recents_table.txt", 'r') as rt_file:
        template = rt_file.read().split("\n")

    recents = db.get_recent_commands(10)

    tables = "\n".join(template[:-1])
    for i in range(10):
        tables = tables + "\n" + pop_recents_row(recents[i], template[-1])

    return tables


def pop_op(game):
    """Populate the OP

    return string Markdown OP text
    """

    with open(TEXT_PATH + "op.txt", 'r') as op_file:
        text = op_file.read()

    namevar = {
        "last_op_update": time.strftime(
            "%a %d-%m-%y, %I:%M:%S%p", time.gmtime()
        ),
        "link_karma": game.get_karma("link"),
        "comment_karma": game.get_karma("comment"),
        "gold": game.get_gold(),
        "top_link_all": db.get_top_karma_type("link", 1)[0]["name"],
        "top_comment_all": db.get_top_karma_type("comment", 1)[0]["name"],
        "top_g_all": db.get_top_karma_type("gold", 1)[0]["name"],
        "top_link_24h": db.get_top_karma_type("link", 1, 24)[0]["name"],
        "top_comment_24h": db.get_top_karma_type("comment", 1, 24)[0]["name"],
        "top_g_24h": db.get_top_karma_type("gold", 1, 24)[0]["name"],
        "link_units": pop_units_list(game.link_units, game),
        "comment_units": pop_units_list(game.comment_units, game),
        "recent_history": pop_recents_list()
    }

    for ref, value in namevar.iteritems():
        text = text.replace("{" + ref + "}", str(value))

    return text


def pop_hs():
    """Populates the highscores page for
    the wiki.

    return string Markdown highscores table text
    """

    pass


def pop_fail(reason):
    """Populates the command fail message

    return string populated text with alts chosen
    """

    with open(TEXT_PATH + "fail_cmd.txt", 'r') as fc_file:
        text = fc_file.read()

    text = text.replace("{reason}", reason)
    text = choose_alts(text)

    return text


def pop_success(action):
    """Populates the command success message

    return string populated text with alts chosen
    """

    with open(TEXT_PATH + "success_cmd.txt", 'r') as sc_file:
        text = sc_file.read()

    text = text.replace("{action}", action)
    text = choose_alts(text)

    return text


def pop_gilded(chance):
    """Populates the command gilded message

    return string populated text with alts chosen
    """

    with open(TEXT_PATH + "success_cmd_gilded.txt", 'r') as scg_file:
        text = scg_file.read()

    text = text.replace("{chance}", chance)
    text = choose_alts(text)

    return text


def pop_stats_request():
    """Populates the reply to a stats request
    with information about _user_.

    """

    pass
