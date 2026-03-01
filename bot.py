import requests
import openai
import schedule
import time

# DALL-E API settings
DALLE_API_URL = 'https://api.openai.com/v1/images/generations'
DALLE_API_KEY = 'your_dalle_api_key'

# GPT-4 API settings
GPT4_API_URL = 'https://api.openai.com/v1/chat/completions'
GPT4_API_KEY = 'your_gpt4_api_key'

# Instagram API settings
INSTAGRAM_API_URL = 'https://graph.instagram.com/me/media'
INSTAGRAM_ACCESS_TOKEN = 'your_instagram_access_token'

# Function to generate an image using DALL-E
def generate_image(prompt):
    response = requests.post(DALLE_API_URL, headers={
        'Authorization': f'Bearer {DALLE_API_KEY}',
        'Content-Type': 'application/json'
    }, json={
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024'
    })
    image_url = response.json()['data'][0]['url']
    return image_url

# Function to generate a caption using GPT-4
def generate_caption(image_url):
    response = requests.post(GPT4_API_URL, headers={
        'Authorization': f'Bearer {GPT4_API_KEY}',
        'Content-Type': 'application/json'
    }, json={
        'model': 'gpt-4',
        'messages': [{
            'role': 'user',
            'content': f'Create a captivating caption for an image: {image_url}'
        }]
    })
    caption = response.json()['choices'][0]['message']['content']
    return caption

# Function to post an image to Instagram
def post_to_instagram(image_url, caption):
    requests.post(INSTAGRAM_API_URL, headers={
        'Authorization': f'Bearer {INSTAGRAM_ACCESS_TOKEN}'
    }, data={
        'image_url': image_url,
        'caption': caption
    })

# Scheduler to post 10 images daily at specific times
def schedule_daily_posts():
    for i in range(10):
        prompt = f'Artistic image {i + 1}'
        image_url = generate_image(prompt)
        caption = generate_caption(image_url)
        post_to_instagram(image_url, caption)

# Schedule posting at 8 AM
schedule.every().day.at('08:00').do(schedule_daily_posts)

while True:
    schedule.run_pending()
    time.sleep(1)
