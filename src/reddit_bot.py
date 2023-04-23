import os
import praw
import prawcore
from praw import exceptions

import generate_image
import generate_prompt

class RebbitBot:
    def __init__(self):
        reddit_client_id = os.environ['reddit_bot_client_id']
        reddit_client_secret = os.environ['reddit_bot_client_secret']
        reddit_user_agent = os.environ['reddit_bot_user_agent']

        reddit_password = os.environ['reddit_bot_password']
        reddit_username = os.environ['reddit_bot_username']

        reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret,
                             password=reddit_password, user_agent=reddit_user_agent,
                             username=reddit_username)

        self.reddit = reddit
        self.rate_limit_history = {}


    def run(self):
        messages = self.reddit.inbox.stream()
        print('mommy im posting')
        for message in messages:
            try:
                if message in self.reddit.inbox.mentions() and message in self.reddit.inbox.unread():
                    if self.check_rate(message.author.name):
                        pic_url = self.generate_image(message.author.name)
                        message.reply(f'If your words were a picture, [this is what you\'d look like]({pic_url}).')
                        print("Just replied to: " + message.author.name)
                    message.mark_read()
            except exceptions.APIException:
                print('whoopsies')


    def check_rate(self, username):
        if username in self.rate_limit_history:
            if self.rate_limit_history[username] < 10:
                self.rate_limit_history[username] += 1
                print(f'user {username} has commented {str(self.rate_limit_history[username])} times')
                return True
            return False
        self.rate_limit_history[username] = 1
        return True


    def generate_image(self,username):
        print('query reddit')
        comments = self.get_all_user_comments(username=username, count=5)
        posts = self.get_all_user_posts(username=username, count=5)

        print(comments)
        print(username)
        cleaned_comments = [(comment['submission_or_parent_content'],
                            comment['comment_content']) for comment in comments]
        cleaned_posts = [(post['submission_title'], post['submission_content']) for post in posts]

        print('create cohere prompt')
        prompt = generate_prompt.format_prompt(cleaned_comments, cleaned_posts)
        print(prompt)
        print('query cohere')
        image_gen_prompt = generate_prompt.generate_prompt(prompt, temp=1) + " portrait, photo realistic, high detail"
        print(image_gen_prompt)

        url = generate_image.generate_image(image_gen_prompt)

        return url


    def get_all_user_comments(self, username, count=20):
        comments = []
        for comment in self.reddit.redditor(username).comments.new(limit=count):
            submission_id = comment.link_id[3:]
            parent_id = comment.parent_id[3:]

            try:
                post = self.reddit.submission(submission_id)
                post_title = post.title
                submission_body = post.selftext

                if len(submission_body) > 1000:
                    submission_body = submission_body[:1000]
                else:
                    submission_body = submission_body

            except prawcore.exceptions.NotFound:
                post = self.reddit.submission(submission_id)
                parent = self.reddit.comment(parent_id)
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


    def get_all_user_posts(self, username, count=20):
        posts = []
        for submission in self.reddit.redditor(username).submissions.new(limit=count):
            if submission.selftext == '':
                continue
            else:
                post = {
                    'subreddit_name': submission.subreddit.display_name,
                    'submission_id': submission.id,
                    'submission_title': submission.title,
                    'submission_content': submission.selftext[:800],
                    'submission_score': round(submission.score),
                    'submission_awards': round(submission.total_awards_received),
                }
                posts.append(post)

        return posts


def main():
    bot = RebbitBot
    bot.run(reply='mommy')


if __name__ == '__main__':
    main()
