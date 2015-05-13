#!/user/bin/env pthon
"""
Karma Tycoon Bot
Reddit integration class
reddit.py

http://karma.matho.me/
"""

import praw, time, os, sys
import texter, user, db
from pprint import pprint

DATA_PATH = "../data/"
CRED_FILE = DATA_PATH + "bot.kt"

class Reddit:
    """Reddit class
    
    For integration with Reddit, is able to
    edit posts, wiki, flair, flair css, get 
    new comments and post replies.
    
    run_loop is the main loop of the program,
    as everything relies on comment input.
    """

    def __init__(self):
        """Connects to Reddit
        
        Identifies with Reddit, loads credentials, logs
        in and instantiates a new Texter object.
        """
        
        if not os.path.exists(CRED_FILE):
            print ":: no bot credential file found in %s" \
                    % CRED_FILE
            print ":: please resolve this error manually."
            print ":: exiting..."
            sys.exit()
        
        with open(CRED_FILE, 'r') as f:
            creds = f.read().split("\n")
            print ":: loaded bot credentials"
            
        try:
            user_agent = "karma-tycoon-controller:v0.5.0 by /u/Toofifty"
            self.r = praw.Reddit(user_agent=user_agent)
            self.r.login(creds[0], creds[1])
            self.sub = self.r.get_subreddit("karmatycoon")
            self.texter = texter.Texter()
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
    
        #for comment in self.sub.get_comments():
        for comment in praw.helpers.comment_stream(reddit_session=self.r, 
                subreddit=self.sub, limit=100):
                
            if not db.has_comment_id(comment.id):
                print ":: found new comment"
                if "karma-tycoon" == comment.link_author \
                        and "karma-tycoon" != comment.author.name:
                    
                    #pprint(vars(comment))
                    comment_user = user.get_user(comment.author.name)
                    
                    success, info, gold = game.parse_command(comment_user, 
                            comment.body)
                    
                    if db.get_command_count(comment_user) == 0:                    
                        if success:
                            # maybe someone will get gold on their first try?
                            if gold:
                                self.reply_gold(comment, info)
                            else:
                                self.reply_success(comment, info)
                        else:
                            self.reply_fail(comment, info)
                            # comment.delete
                            continue
                    else:
                        if not success:
                            self.reply_fail(comment, info)
                            # comment.delete
                            continue
                        elif gold:
                            self.reply_gold(comment, info)
                    
                    self.update_op(game)
                    self.update_user_flair(user)
                    
                db.add_comment_id(comment.id)
                    
            time.sleep(2)
        
        
    def update_op(self, game):
        """Update the original post, populated with
        values from _game_, and the db.
        """
        
        text = self.texter.pop_op(game)
        pass
        
        
    def update_hs(self):
        """Update the highscores page on the wiki,
        populated with values from the db.
        """
        
        pass
        
        
    def update_user_flair(self, user):
        """Update a user's flair and flair css,
        populate with _user.get_flair()_ and
        _user.get_flair_css()_
        """
        
        pass
        
        
    def reply_fail(self, comment, reason):
        """Reply a fail message to the comment given,
        that is populated with _reason_.
        """
        
        try:
            comment.reply(self.texter.pop_fail(reason))
        except:
            pass
        
        
    def reply_success(self, comment, action):
        """Reply a success message to the comment given,
        that is populated with _action_.
        """
        
        try:
            comment.reply(self.texter.pop_success(action))
        except:
            pass
        
        
    def reply_gilded(self, comment, chance):
        """Reply a gilded message to the comment given,
        that is populated with _chance_.
        """
        
        try:
            comment.reply(self.texter.pop_gilded(chance))
        except:
            pass
            