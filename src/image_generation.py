import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

SAMPLE_PROMPT = 'A close up, studio photographic portrait. This person is walking with a cane. They are old and slow, and they look sad. They are wearing a black coat.'

def generate_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            size='1024x1024',
            response_format='url'
        )

        print(response['data'][0]['url'])
    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)

def main():
    generate_image(SAMPLE_PROMPT)

if __name__ == '__main__':
    main()
