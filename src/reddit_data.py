# Import libraries
import os

# Reddit API
import praw
import prawcore

reddit_client_id = os.getenv('reddit_client_id')
reddit_client_secret = os.getenv('reddit_client_secret')
reddit_user_agent = os.getenv('reddit_user_agent')

# create a reddit instance using the API key
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent)

# function to get all posts from a user


def getAllUserPosts(username, count=20):
    """
    Function to get all posts from a user

    Params:
    --------
    username: Reddit username

    Return:
    --------
    posts: list of dictionaries
    """

    posts = []
    for submission in reddit.redditor(username).submissions.new(limit=count):
        if submission.selftext == '':
            continue
        else:
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

# function to get all comments from a user and parent post/coment
def getAllUserComments(username, count=20):
    """
    Function to get all comments from a user and parent post/coment

    Params:
    --------
    username: Reddit username

    Return:
    --------
    comments: list of dictionaries
    """

    comments = []
    for comment in reddit.redditor(username).comments.new(limit=count):
        submission_id = comment.link_id[3:]
        parent_id = comment.parent_id[3:]

        try:
            post = reddit.submission(submission_id)
            post_title = post.title
            submission_body = post.selftext
            
            if len(submission_body) > 1000:
                submission_body = submission_body[:1000]
            else:
                submission_body = submission_body

        except prawcore.exceptions.NotFound:
            post = reddit.submission(submission_id)
            parent = reddit.comment(parent_id)
            post_title = post.title
            submission_body = parent.body

        comment = {
            'subreddit_name': comment.subreddit.display_name,
            'submission_id': submission_id,
            'parent_id': parent_id,
            'comment_id': comment.id,
            'comment_content': comment.body,
            'comment_score': round(comment.score),
            'comment_awards': round(comment.total_awards_received),
            'post_title': post_title,
            'submission_or_parent_content': submission_body,
        }
        comments.append(comment)

    return comments
