#!/user/bin/env pthon
"""
Karma Tycoon Bot
Reddit integration class
reddit.py

http://karma.matho.me/
"""

import praw, time, os, sys
import texter, user, db

DATA_PATH = "../data/"
CRED_FILE = DATA_PATH + "bot.kt"

SM_ID = "35wp1j"

class Reddit(object):
    """Reddit class

    For integration with Reddit, is able to
    edit posts, wiki, flair, flair css, get
    new comments and post replies.

    run_loop is the main loop of the program,
    as everything relies on comment input.
    """

    def __init__(self):
        """Connects to Reddit

        Identifies with Reddit, loads credentials,
        and logs in.
        """

        if not os.path.exists(CRED_FILE):
            print ":: no bot credential file found in %s" \
                    % CRED_FILE
            print ":: please resolve this error manually."
            print ":: exiting..."
            sys.exit()

        with open(CRED_FILE, 'r') as c_file:
            creds = c_file.read().split("\n")
            print ":: loaded bot credentials"

        try:
            user_agent = "karma-tycoon-controller:v0.5.0 by /u/Toofifty"
            self.reddit = praw.Reddit(user_agent=user_agent)
            self.reddit.login(creds[0], creds[1])
            self.subr = self.reddit.get_subreddit("karmatycoon")
            self.subm = self.reddit.get_submission(submission_id=SM_ID)
            print ":: ready for Reddit input"

        except praw.requests.exceptions.ConnectionError:
            print ":: failed to connect to Reddit"
            print ":: exiting..."
            sys.exit()


    def run_loop(self, game):
        """Main Reddit input loop.

        Gets comments, ensures comment is new and not made
        by "karma-tycoon", parses the command and replies
        with an appropriate response.

        Sleeps 2 seconds after each comment. If this is too
        slow, nesting this loop in a while loop may be the
        way to go.
        """

        #for comment in self.subr.get_comments():
        for comment in praw.helpers.comment_stream(
                reddit_session=self.reddit, subreddit=self.subr, limit=100
            ):

            if not db.has_comment_id(comment.id):
                if "karma-tycoon" == comment.link_author \
                        and "karma-tycoon" != comment.author.name:

                    comment_user = user.get_user(comment.author.name)
                    command_count = db.get_command_count(comment_user)

                    print ":: new comment %s by %s (%d)" % (
                        comment.id, comment.author.name, command_count
                    )

                    success, info, gold = game.parse_command(
                        comment_user, comment.body
                    )

                    if not info == "not command":
                        if success:
                            # maybe someone will get gold on their first try?
                            if gold:
                                self.reply_gilded(comment, info)
                                print ":: %s was gilded!" % comment.author.name
                            else:
                                self.reply_success(comment, info)
                        else:
                            self.reply_fail(comment, info)

                    self.update_op(game)
                    self.update_user_flair(comment_user)
                    db.update_user(comment_user)
                    db.update_game(game)

                print ":: adding %s to db" % comment.id
                db.add_comment_id(comment.id)
                time.sleep(2)


    def update_op(self, game):
        """Update the original post, populated with
        values from _game_, and the db.
        """

        text = texter.pop_op(game)
        self.subm.edit(text)


    def update_hs(self):
        """Update the highscores page on the wiki,
        populated with values from the db.
        """

        pass


    def update_user_flair(self, usr):
        """Update a user's flair and flair css,
        populate with _user.get_flair()_ and
        _user.get_flair_css()_
        """

        if db.get_position(usr) <= 20:
            # May need to shift others
            self.update_top_20_flairs()
        else:
            self.subr.set_flair(
                usr.name, usr.get_flair(), usr.get_flair_css()
            )


    def update_top_20_flairs(self):
        """Update the flairs of the top 20 players,
        as we want to shift these when someone in the
        top 20 moves.
        """

        flairs = []
        for data in db.get_top_karma(20, None):
            usr = user.get_user(data["name"])
            flairs.append({
                "user": usr.name,
                "flair_text": usr.get_flair(),
                "flair_css_class": usr.get_flair_css()
            })

        self.subr.set_flair_csv(flairs)

    def reply_fail(self, comment, reason):
        """Reply a fail message to the comment given,
        that is populated with _reason_.
        """

        comment.reply(texter.pop_fail(reason))


    def reply_success(self, comment, action):
        """Reply a success message to the comment given,
        that is populated with _action_.
        """

        comment.reply(texter.pop_success(action))


    def reply_gilded(self, comment, chance):
        """Reply a gilded message to the comment given,
        that is populated with _chance_.
        """

        comment.reply(texter.pop_gilded(chance))
