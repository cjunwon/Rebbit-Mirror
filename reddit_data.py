# Import libraries
import os
import pandas as pd
from dotenv import load_dotenv

# Reddit API
import praw

# Load environment variables
load_dotenv()

reddit_client_id = os.getenv('reddit_client_id')
reddit_client_secret = os.getenv('reddit_client_secret')
reddit_user_agent = os.getenv('reddit_user_agent')

# create a reddit instance using the API key
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent)

# function to get all posts from a user

def getAllUserPosts(r, username, count=20):

    """
    Function to get all posts from a user

    Params:
    --------
    r: Reddit instance
    username: Reddit username

    Return:
    --------
    posts: list of dictionaries
    """

    posts = []
    for submission in r.redditor(username).submissions.new(limit=count):
        post = {
            'subreddit_name': submission.subreddit.display_name,
            'submission_id': submission.id,
            'submission_title': submission.title,
            'submission_content': submission.selftext,
            'submission_score': round(submission.score),
            'submission_awards': round(submission.total_awards_received),
        }
        posts.append(post)
    return posts