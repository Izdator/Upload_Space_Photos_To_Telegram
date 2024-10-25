from datetime import datetime, timedelta
import json
import os
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests

from general_functions import download_pictures, detect_file_extension


def get_astronomy_picture_of_the_day(api_key, count=30):
    base_url = "https://api.nasa.gov/planetary/apod"
    image_urls = []
    date_today = datetime.now()

    os.makedirs('images', exist_ok=True)

    for _ in range(count):
        params = {
            'api_key': api_key,
            'date': date_today.strftime('%Y-%m-%d'),
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        apod_data = response.json()

        if 'url' in apod_data:
            image_urls.append(apod_data['url'])
            image_extension = detect_file_extension(apod_data['url'])
            image_name = f'images/nasa_apod_{date_today.strftime("%Y%m%d")}{image_extension}'
            try:
                download_pictures(apod_data['url'], image_name)
            except (requests.exceptions.RequestException, IOError) as e:
                print(f"Error downloading image from {apod_data['url']}: {e}")

        date_today = date_today - timedelta(days=1)

    return image_urls


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ['NASA_TOKEN']
    urls_apod = get_astronomy_picture_of_the_day(api_key)
