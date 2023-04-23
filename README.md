> A person who has good thoughts cannot ever be ugly. You can have a wonky nose and a crooked mouth and a double chin and stick-out teeth, but if you have good thoughts it will shine out of your face like sunbeams and you will always look lovely. - Roald Dahl

## Inspiration

We 👦💰 😱😙 spend 🎈 🎈 a lottt of time 🐢 🤣 on 🔥 🥵 our 💩 ✂️✂️ favorite 😘😍 👏 website, Rebbit. Often 💰 🍆💰💰 times, 🕐😆 💦 we 👩‍👩‍👦‍👦 👩‍👩‍👦‍👦 wonder 😮 😮 what 👏😱 👏 some 👨💭 🍯🤔 of our 💩 💦💩 dear 🔆 🔆 redditor friends 🐷 🐷 and colleagues look 🎱 🧐 like 🤮 😛 in 💁 ⭐ real 😾 😾 life. 🔈🌎 😂👨 Sometimes, 🕐 ✨ these 🌍 🍆 people 👫 👨 have 😣✅ 👃🈶 wacky 😜 😜 posts 📱💻 📱💻 and comments that 🤒 🍆 really 😕 👷🏼💳🚡 allow 👨‍👨‍👦‍👦🎫🎫 👨‍👨‍👦‍👦🎫🎫 for 😘 😊 their 🍷 😴 real 🔎 😼 personality to shine! ✨✨✨ ✨✨✨ We 👩‍👩‍👦‍👦 💏🏼 hope 🙏 🙏🏼👏🏼 to find 🔎🔎🔎🔎 🔍 out 😵😵 😰 what 😦 😦 our 💰 💰👶 friends 👯👯‍♂️👯‍♀️ 👥 look 👀 👁️‍🗨️ like 😗 💒😄 in 🙌👏 👉 real 📷 💯 life! 😛 🧬. I am so scawwed.

## What it does

When tagged, our Reddit bot creates a photorealistic image of a user based on their history of posts and comments on Reddit.

## How we built it

For this project, we utilized Python as our primary programming language and Cohere's language model and the DALL-E API to generate photorealistic images of Reddit users. **we fine-tuned co:here generate endpoint to produce descriptive DALL-E prompts to generate the images based on reddit history.** It was interesting to engineer our prompts so that the co:here model could understand an Internet conversation and infer dispositions.

Our Python scripts fetch user data through the Reddit API, create a prompt that feeds into Cohere's generative language model API, which then outputs an optimized prompt to feed into OpenAI's DALL-E model. The resulting image is photorealistic and encapsulates the user's characteristics based on their online presence. We hosted our entire pipeline on Docker, which simplified deployment and testing.

## Challenges we ran into

A primary challenge that we faced was guiding Cohere to generate a prompt for DALL-E in a consistent manner. Using Cohere's model training feature, we fed a dataset of formatted yet diversified prompts that were descriptive and optimized for DALL-E image generation. After training Cohere's generative language model, we achieved successful results that were consistent and descriptive.

## Accomplishments that we're proud of
What man could sleep at the end of the day, proud of what little he accomplished is this cosmic masquerade we call life.


## What we learned
- Reddit API (PRAW)
- Cohere
- What DALL-E likes

## What's next for Reddit Mirror
-More fine tuning for the model will be needed, so that our images can get more sentiment behind them
-Current models don't return as descriptive an image that they could. We need more tags that can be translated by Dall-E.

> The portrait would be to him the most magical of mirrors. As it had revealed to him his own body, so it would reveal to him his own soul. - Oscar Wilde 
