import reddit_data
import generate_prompt
import image_generation


def main():
    print("cock n balls")
    username = "brokenjago"
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
    print(image_gen_prompt)
    url = image_generation.generate_image(image_gen_prompt)
    print(url)


if __name__ == '__main__':
    main()
