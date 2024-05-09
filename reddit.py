import praw
import csv
import re

#create a reddit read-only instance
reddit = praw.Reddit(
    client_id = '',
    client_secret = '',
    user_agent = ''
)
#check connection
print(reddit.read_only)

#output file
csvfile2 = open('reddit_scrapped.csv', 'w', newline ='')
writer = csv.writer(csvfile2)
#write the headers
writer.writerow(['subreddit', 'title', 'comments'])

#bots to exclude
bots = ['AutoModerator']

def preprocess(txt):
    #remove links
    txt = re.sub('https.+', '', txt)
    #take only ascii characters
    txt = ''.join([ch if ord(ch)<=127 else '' for ch in txt])

    return txt

for submission in reddit.subreddit('all').search('vaccine hesitancy'):
    i = 0
    submission.comments.replace_more(limit=15) #15 is the depth of comment level that is considered

    print(f'Working with {submission.title} ...')

    for comment in submission.comments.list(): #using BFS all the comments will be parsed
        i += 1
        if i > 1800: break
        if comment.author and comment.author not in bots:
            txt = preprocess(comment.body)
            if txt:
                writer.writerow([submission.subreddit, submission.title, txt])