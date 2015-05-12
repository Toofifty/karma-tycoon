import praw
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
        print ":: ready for Reddit input"
        
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
        
    def load_completed(self):
        fn = "comments.kt"
        with open(DATA_PATH + fn, 'r') as f: 
            self.completed = f.read().split("\n")
            
    def save_completed(self):
        fn = "comments.kt"
        with open(DATA_PATH + fn, 'w') as f:
            f.write("\n".join(self.completed))