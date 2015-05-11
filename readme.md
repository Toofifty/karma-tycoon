# Karma Tycoon

[Subreddit](http://www.reddit.com/r/karmatycoon/) | [Bot](http://www.reddit.com/u/karma-tycoon/) | Thread (coming soon)

## How it'll work

It's So Meta, Even This Acronym

Like any tycoon game, there will be a currency. In this case, it's karma. You use karma to purchase post types (i.e. kitten pictures, reposts, sneaky referential comments, in-jokes) that will increase production of karma. Higher-level units (AMAs, test posts please ignore) will cost increasingly more karma and take longer to profit, though profits will be much larger. As upgrades are bought they will exponentially increase in price.

There are two karma types: links and comments. At the moment they work identically, though this may be changed in the future. You will be free to add to both point totals, if you wish.

Reddit Gold will also be a currency, that will be able to purchase speed upgrades for the units. It will be added randomly when "posting" a link or comment in the game, with higher payouts having a larger chance of awarding Gold. There will be only one Gold total.

There will be a stickied thread on [/r/karmatycoon](http://www.reddit.com/r/karmatycoon/) which will serve as a way to see the current karma, upgrades, and instructions. Comments in this thread will be actions (buy 1 kitten-post, comment on niche-subreddit-thread, etc) that will influence upgrades and karma. The bot will reply to these comments, indicating whether the action was successful or not (if the cooldown time of a post hasn't finished, for example). The OP will be updated very regularly.

The rest of the subreddit is open to the public for discussion about the game, strategies and circle-jerks.

Users will have a flair that shows how much karma they have added to the total (through links and comments) and the gold they have randomly received. They will be able to see these stats and the specific upgrades/units bought through a comment or message directed to the bot.

There will be no cap on the amount of karma, and more units will probably be added when the karma gets out of hand. Votes to reset the karma may be an option every once in a while.

## The units

### Comments

| Multipliers | Cost                   | Cooldown          | Payoff           |
|-------------|-----------------------:|------------------:|-----------------:|
| Buy unit    |                 `1.45` |             `N/A` |            `1.3` |
| Next unit   | `2 x 5.4417 x ?? 2.5n` | `15.1414 x ?? 1n` | `4.8599 x ?? 2n` |

| n  | Comment name                       | Alt     | Cost    | Cooldown    | Payoff |
|---:|------------------------------------|---------|--------:|-------------|-------:|
|  1 | Late to the party                  | `party` |       2 |    1 second |      1 |
|  2 | Unpopular opinion                  | `unpop` |      30 |  16 seconds |      7 |
|  3 | Niche subreddit, overlooked thread | `niche` |      90 |  45 seconds |     15 |
|  4 | Thoughtful response                | `thoug` |     210 | 110 seconds |     28 |
|  5 | Unsuccessful circlejerk            | `badcj` |     430 | 240 seconds |     46 |
|  6 | Unsuccessful meme                  | `umeme` |     800 | 440 seconds |     72 |
|  7 | First comment on niche thread      | `pop-n` |    1420 |  13 minutes |    108 |
|  8 | Relevant video                     | `video` |    2400 |  25 minutes |    157 |
|  9 | Reddit fame overlooked             | `rfovr` |    3950 |  40 minutes |    222 |
| 10 | Pointing out overused meme         | `memeo` |    6200 |  60 minutes |    309 |
| 11 | Weed reference                     | `weeds` |    9420 |  90 minutes |    420 |
| 12 | Overused meme                      | `omeme` |   14500 | 140 minutes |    565 |
| 13 | Popular opinion                    | `popop` |   21500 | 200 minutes |    748 |
| 14 | Reddit fame spotted                | `rfame` |   31300 |     5 hours |    980 |
| 15 | Top comment in a niche thread      | `top-n` |   45000 |     7 hours |   1270 |
| 16 | Cool /r/AskReddit story, bro       | `ask-r` |   64000 |    10 hours |   1633 |
| 17 | Funny typo                         | `typoo` |   90000 |    15 hours |   2081 |
| 18 | Scientific response                | `scien` |  125000 |    20 hours |   2633 |
| 19 | Default subreddit, first comment   | `first` |  172000 |    30 hours |   3308 |
| 20 | Mentioned on /r/bestof             | `besto` |  240000 |    40 hours |   4130 |
| 21 | Default subreddit, funny comment   | `funny` |  320000 |      2 days |   5126 |
| 22 | Top post in a default              | `topdf` |  425000 |      3 days |   6331 |
| 23 | President's AMA, first comment     | `p-ama` |  575000 |      4 days |   7779 |
| 24 | Test comment please ignore         | `testp` |  760000 |      5 days |   9514 |
| 25 | Reddit famous AMA                  | `i-ama` | 1000000 |      7 days |  11586 |

### Links (re)posts

| n  | Post name                           | Alt     | Cost    | Cooldown    | Payoff |
|---:|-------------------------------------|---------|--------:|-------------|-------:|
|  1 | Downvoted in /r/new                 | `r-new` |       2 |    1 second |      1 |
|  2 | Okay post to niche subreddit        | `okayn` |      30 |  16 seconds |      7 |
|  3 | Self promotion                      | `promo` |      90 |  45 seconds |     15 |
|  4 | Quality link in niche subreddit     | `niche` |     210 | 110 seconds |     28 |
|  5 | Quality link in default subreddit   | `qdflt` |     430 | 240 seconds |     46 |
|  6 | News-worthy article                 | `newsa` |     800 | 440 seconds |     72 |
|  7 | Mention in /r/shitposts             | `shitp` |    1420 |  13 minutes |    108 |
|  8 | Shitty image in default subreddit   | `shiti` |    2400 |  25 minutes |    157 |
|  9 | Passive aggressive image            | `passi` |    3950 |  40 minutes |    222 |
| 10 | Kitten picture on /r/Aww            | `kitty` |    6200 |  60 minutes |    309 |
| 11 | Repost to default subreddit         | `rpost` |    9420 |  90 minutes |    415 |
| 12 | "Happened a year ago" TIFU          | `lyifu` |   14500 | 140 minutes |    565 |
| 13 | Sob story                           | `sobby` |   21500 | 200 minutes |    748 |
| 14 | Meta about beating a dead horse     | `hmeta` |   31300 |     5 hours |    980 |
| 15 | Beating a dead horse                | `horse` |   45000 |     7 hours |   1270 |
| 16 | Cool gif                            | `giffy` |   64000 |    10 hours |   1633 |
| 17 | Self promotion (famous)             | `adver` |   90000 |    15 hours |   2081 |
| 18 | vernetroyer                         | `verne` |  125000 |    20 hours |   2633 |
| 19 | Picture of hot girl                 | `hotty` |  172000 |    30 hours |   3308 |
| 20 | Niche post mentioned in /r/bestof   | `besto` |  240000 |    40 hours |   4130 |
| 21 | Participate in site-wide circlejerk | `cjerk` |  320000 |      2 days |   5126 |
| 22 | Shitpost to /r/AdviceAnimals        | `smeme` |  425000 |      3 days |   6331 |
| 23 | Top of /r/all/                      | `r-all` |  575000 |      4 days |   7779 |
| 24 | Become a meme                       | `me-me` |  760000 |      5 days |   9514 |
| 25 | Test post please ignore             | `testp` | 1000000 |      7 days |  11586 |
