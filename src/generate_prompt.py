from os import environ
import cohere

import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')

# import the environment variable COHERE_TRIAL_KEY

# set the trial key
trial_key = environ['COHERE_PROD_KEY']
co = cohere.Client(trial_key)  # This is your trial API key


def format_comment(previous: str, reply: str) -> str:
    """Format a comment from Reddit for Cohere prompting."""
    return f"Someone else said: {previous}\nAnd this user replied: {reply}"


def format_post(title: str, post: str) -> str:
    """Format a post from Reddit for Cohere prompting."""
    return f"Post title: {title}\nPost content: {post}"


def format_prompt(comments, posts):
    prompt = "I will provide posts and comments made by one specific user on Reddit. You will create an image of the user based on their posts.\n\n"

    for previous, reply in comments:
        prompt += format_comment(previous, reply)
        prompt += "\n\n"

    prompt += "Now I will provide posts from this one specific user.\n\n"

    for title, content in posts:
        # prompt += "POST\n"
        prompt += format_post(title, content)
        prompt += "\n\n"

    prompt += "Using the comments and posts made by this specific user, analyze their characteristics, personality, and word use to write me a prompt to generate one image of the person. The prompt should describe the user's face, facial hair, body, emotions, what they are doing, and their surroundings.\n\nThe prompt:"

    return prompt


def generate_prompt(prompt, temp=1.5):
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=270,
        temperature=temp,
        # num_generations=5,
        k=0,
        # stop_sequences=["\n"],
        return_likelihoods='NONE')

    return response.generations[0].text


def remove_stopwords(text: str):
    # Lowercase the input text
    text = text.lower()

    # Use a set for faster lookups
    stop_words = set(stopwords.words('english'))
    stop_words.add("digital")
    stop_words.add("illustration")

    # Filter out any stopwords
    words = filter(lambda word: word not in stop_words, text.split(sep=' '))

    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    # Join the remaining words back into a string
    cleaned_text = ' '.join(unique_words)

    return cleaned_text


if __name__ == "__main__":
    response_beginning = "This person is"
    posts = [
        ("Neighbors Constantly Asking for Access to My Property", "My neighbors are pretty overbearing. Their kids throw loud parties, their dogs bark constantly, and they have cut down every tree along the property line leaving absolutely no privacy, and have installed every possible obnoxious structure along the property line to encourage constant noise, odors and flies to come onto my property.\n\nNow they have started something new.\n\nThey constantly ask for access to my property. They will spy on what is in my backyard. One time it was a pile of firewood that I wasn\'t using. They asked to bring their truck through my property to collect the firewood to use for an \"art project.\" I said no. It would require me to move multiple vehicles in my driveway, and in the backyard so she can fit her truck through the gate. Stay on your own land, and if you want to do an art project, get firewood yourself."),
        ("Dead friend lmao", "I had a good friend that was sick for a month with cold like symptoms. The doctor kept telling him it was just a cold. He kept get getting a fever of 104ish that would come and go. He complained a lot about being sick and we knew something was wrong and told him this wasn\'t normal. A week or two later, he died. The COD was pneumonia and sepsis. Had he had more classic symptoms and a better doctor, he would have gone to the hospital.")
    ]
    comments = [
        ("https://abc7.com/thousand-oaks-westlake-high-school-ventura-county-california/13151121/ this article recently updated to state that 1 person (15yo boy) is dead as a result of this 😭 my condolences to everyone in the community who was affected (i never went to this school but my little brother currently does",
         "I just saw this post as we were leaving the Promenade -- TO Blvd is still closed. How horrible. No words."),
        ("This will get shut down by the higher courts. No way this stands.",
         "It will be upheld by the Trump Supreme Court.")
    ]
    prompt = format_prompt(comments, posts, response_beginning)
    print(prompt)
    output = generate_prompt(prompt, temp=1) + " portrait, photo realistic, high detail"
    print(output)
    cleaned_output = remove_stopwords(output)
    print(cleaned_output)
