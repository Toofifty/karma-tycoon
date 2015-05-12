import praw, time
import texter, user
from pprint import pprint

DATA_PATH = "../data/"

class Reddit:
    def __init__(self):
        # connect to reddit
        
        self.load_completed()
        user_agent = "karma-tycoon-controller:v0.5.0 by /u/Toofifty"
        self.r = praw.Reddit(user_agent=user_agent)
        
        fn = "bot.kt"
        with open(DATA_PATH + fn, 'r') as f:
            creds = f.read().split("\n")
            
        self.r.login(creds[0], creds[1])
        self.sub = self.r.get_subreddit("karmatycoon")
        self.texter = texter.Texter()
        print ":: ready for Reddit input"
        
        
    def run_loop(self, game, stats, history):
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
                            continue
                        elif gold:
                            self.reply_gold(comment, info)
                    
                    self.update_op(game, stats, history)
                    
            time.sleep(2)
        
    def next_comment(self):
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
        self.completed.append(cID)
        self.save_completed()
        
        
    def load_completed(self):
        fn = "comments.kt"
        with open(DATA_PATH + fn, 'r') as f: 
            self.completed = f.read().split("\n")
            
            
    def save_completed(self):
        fn = "comments.kt"
        with open(DATA_PATH + fn, 'w') as f:
            f.write("\n".join(self.completed))
            
            
    def update_op(self, game, stats, history):
        text = self.texter.pop_op(game, stats, history)
        pass
        
        
    def update_hs(self, stats):
        # TODO
        pass
        
        
    def reply_fail(self, comment, reason):
        try:
            comment.reply(self.texter.pop_fail(reason))
        except:
            pass
        
        
    def reply_success(self, comment, action):
        try:
            comment.reply(self.texter.pop_success(action))
        except:
            pass
        
        
    def reply_gilded(self, comment, chance):
        try:
            comment.reply(self.texter.pop_gilded(chance))
        except:
            pass
            