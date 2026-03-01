import requests
import json
import logging
import schedule
import time
import random
from datetime import datetime

# Configure logging
logging.basicConfig(filename='workspace_bot.log', level=logging.INFO)

class InstagramBot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.imgur_client_id = 'YOUR_IMGUR_CLIENT_ID'
        self.themed_workspaces = [
            'Nature', 'Technology', 'Art', 'Fashion', 'Food',
            'Travel', 'Music', 'Fitness', 'DIY', 'Education'
        ]
        self.hashtag_sets = [
            ['#art', '#creativity', '#inspiration'],
            ['#nature', '#photography', '#landscape'],
            ['#fashion', '#style', '#trending'],
            ['#food', '#delicious', '#foodie'],
            ['#travel', '#adventure', '#explore']
        ]

    def generate_image(self, prompt):
        try:
            response = requests.post('https://api.openai.com/v1/images/generations',
                                     headers={'Authorization': f'Bearer {self.access_token}'},
                                     json={'prompt': prompt})
            return response.json()['data'][0]['url']
        except Exception as e:
            logging.error(f'Error generating image: {e}')

    def post_to_instagram(self, image_url, caption):
        payload = {'image_url': image_url, 'caption': caption}
        response = requests.post('https://graph.instagram.com/me/media',
                                 headers={'Authorization': f'Bearer {self.access_token}'},
                                 json=payload)
        return response.json()

    def upload_to_imgur(self, image_path):
        headers = {'Authorization': f'Client-ID {self.imgur_client_id}' }
        with open(image_path, 'rb') as img:  
            response = requests.post('https://api.imgur.com/3/image', headers=headers, data=img)
            return response.json()['data']['link']

    def caption_generation(self, theme):
        return f'This is a {theme} themed post.'

    def run_daily(self):
        for theme in self.themed_workspaces:
            image_url = self.generate_image(theme)
            caption = self.caption_generation(theme)
            self.post_to_instagram(image_url, caption)

    def scheduler(self):
        schedule.every().day.at("09:00").do(self.run_daily)
        while True:
            schedule.run_pending()
            time.sleep(60)  

if __name__ == '__main__':
    bot = InstagramBot('YOUR_INSTAGRAM_ACCESS_TOKEN')
    mode = input('Enter mode (test/immediate): ')
    if mode == 'test':
        print('Running in test mode. No posts will be made.')
        # Implement test mode logic here
    else:
        bot.scheduler()