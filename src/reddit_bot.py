import os
import praw

import reddit_data
import generate_image
import generate_prompt

reddit_client_id = os.getenv('reddit_bot_client_id')
reddit_client_secret = os.getenv('reddit_bot_client_secret')
reddit_user_agent = os.getenv('reddit_bot_user_agent')

reddit_password = os.getenv('reddit_bot_password')
reddit_username = os.getenv('reddit_bot_username')

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret,
                     password=reddit_password, user_agent=reddit_user_agent,
                     username=reddit_username)


class RebbitBot:
    myReddit = reddit
    rateLimitHistory = {}

    def run_bot(self):
        messages = reddit.inbox.stream()
        print("mommy im posting")
        for message in messages:
            try:
                if message in reddit.inbox.mentions() and message in reddit.inbox.unread():
                    if self.check_rate(message.author.name):
                        pic_url = self.generate_image(message.author.name)
                        message.reply(
                            "Bro Is this You? \n [Ugly Aah Dude](" + pic_url+")")
                    message.mark_read()
            except praw.exceptions.APIException:
                print("whoopsies")

    def check_rate(self, username):
        if username in self.rateLimitHistory:
            if self.rateLimitHistory[username] < 10:
                self.rateLimitHistory[username] += 1
                print("user " + username + " has commented " + str(self.rateLimitHistory[username]) + " times")
                return True
            return False
        self.rateLimitHistory[username] = 1
        return True

    def generate_image(self,username):
        print("query reddit")
        comments = reddit_data.getAllUserComments(username=username, count=5)
        posts = reddit_data.getAllUserPosts(username=username, count=5)
        print(comments)
        print(username)
        cleaned_comments = [(comment["submission_or_parent_content"],
                            comment["comment_content"]) for comment in comments]
        cleaned_posts = [
            (post["submission_title"], post["submission_content"]) for post in posts]
        response_beginning = "This person is"
        print("create cohere prompt")
        prompt = generate_prompt.format_prompt(
            cleaned_comments, cleaned_posts, response_beginning)
        print(prompt)
        print("query cohere")
        image_gen_prompt = generate_prompt.generate_prompt(prompt)
        url = generate_image.generate_image(image_gen_prompt)
        print(image_gen_prompt)
        return url


def main():
    bot = RebbitBot
    bot.run_bot(reply="mommy")


if __name__ == '__main__':
    main()
