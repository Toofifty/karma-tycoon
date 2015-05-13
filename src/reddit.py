#!/user/bin/env pthon
"""
Karma Tycoon Bot
Reddit integration class
reddit.py

http://karma.matho.me/
"""

import praw, time, os, sys
import texter, user
from pprint import pprint

DATA_PATH = "../data/"
SAVE_FILE = DATA_PATH + "comments.kt"
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
        
        if not os.path.exists(SAVE_FILE):
            print ":: no comment tracking file found, creating new"
            self.create_save_file()
            
        self.load_completed()
        
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
        
        
    def run_loop(self, game, stats, history):
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
                
            if not comment.id in self.completed:
                print ":: found new comment"
                self.addID(comment.id)
                if "karma-tycoon" == comment.link_author \
                        and "karma-tycoon" != comment.author.name:
                    
                    pprint(vars(comment))
                    comment_user = user.get_user(comment.author.name)
                    
                    success, info, gold = game.parse_command(comment_user, 
                            comment.body, history)
                    
                    if user.commands == 0:                    
                        if success:
                            # maybe someone will get gold on their first try?
                            if gold:
                                self.reply_gold(comment, info)
                            else:
                                self.reply_success(comment, info)
                    else:
                        if not success:
                            self.reply_fail(comment, info)
                            # comment.delete
                            continue
                        elif gold:
                            self.reply_gold(comment, info)
                    
                    self.update_op(game, stats, history)
                    self.update_user_flair(user, stats)
                    
            time.sleep(2)
    
    
    def next_comment(self):
        # Unused.
        for comment in praw.helpers.comment_stream(reddit_session=self.r, 
                subreddit=self.sub, limit=100):
                
            print ":: found comment"
            if not comment.id in self.completed:
                self.completed.append(comment.id)
                self.save_completed()
                if "karma-tycoon" == comment.link_author and "karma-tycoon" != comment.author.name:
                    pprint(vars(comment))
                    comment.reply("hey!")
                    return {"user": comment.author.name, 
                            "comment": comment.body.lower()}
        print ":: no comment. sleeping..."
        return None
        
        
    def addID(self, cID):
        """Add id to completed list, and save."""
    
        self.completed.append(cID)
        self.save_completed()
        
    
    def create_save_file(self):
        """Creates a new completed list file
        
        RESETS CURRENT SAVE
        
        Only to be used if current save 
        isn't found.
        """
        
        with open(SAVE_FILE, 'w') as f:
            f.write("")
        
    def load_completed(self):
        """Load list of completed comments from file."""
    
        with open(SAVE_FILE, 'r') as f: 
            self.completed = f.read().split("\n")
            
            
    def save_completed(self):
        """Save list of completed comments to file."""
        
        with open(SAVE_FILE, 'w') as f:
            f.write("\n".join(self.completed))
            
            
    def update_op(self, game, stats, history):
        """Update the original post, populated with
        values from _game_, _stats_, and _history_.
        """
        
        text = self.texter.pop_op(game, stats, history)
        pass
        
        
    def update_hs(self, stats):
        """Update the highscores page on the wiki,
        populated with values from _stats_.        
        """
        
        pass
        
        
    def update_user_flair(self, user, stats):
        """Update a user's flair and flair css,
        populate with _user.get_flair(stats)_ and
        _user.get_flair_css(stats)_
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
            