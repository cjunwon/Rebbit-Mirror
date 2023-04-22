import os
import praw

reddit_client_id = os.getenv('reddit_bot_client_id')
reddit_client_secret = os.getenv('reddit_bot_client_secret')
reddit_user_agent = os.getenv('reddit_bot_user_agent')

reddit_password = os.getenv('reddit_bot_password')
reddit_username = os.getenv('reddit_bot_username')

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret,
                    password=reddit_password, user_agent=reddit_user_agent,
                    username=reddit_username)


def run_bot(reddit):
    messages = reddit.inbox.stream()
    print("mommy")
    for message in messages:
        try:
            if message in reddit.inbox.mentions() and message in reddit.inbox.unread():
                message.reply("i love cheeto dust on my titties")
                message.mark_read()
        except praw.exceptions.APIException:
            print("whoopsies")


def main():
    run_bot(reddit)

if __name__ == '__main__':
    main()