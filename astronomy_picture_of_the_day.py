from datetime import datetime, timedelta
import json
import os
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests

from general_functions import download_picture, detect_file_extension


def get_astronomy_picture_of_the_day(api_key, count=30):
    base_url = "https://api.nasa.gov/planetary/apod"
    image_urls = []
    date_today = datetime.now()

    os.makedirs('images', exist_ok=True)

    dates = [(date_today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(count)]

    for date in dates:
        params = {
            'api_key': api_key,
            'date': date,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        apod_content = response.json()

        if 'url' in apod_content:
            image_urls.append(apod_content['url'])
            image_extension = detect_file_extension(apod_content['url'])
            image_name = f'images/nasa_apod_{date.replace("-", "")}{image_extension}'

            try:
                download_picture(apod_content['url'], image_name)
            except (requests.exceptions.RequestException, IOError) as e:
                print(f"Error downloading image from {apod_content['url']}: {e}")

    return image_urls


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ['NASA_TOKEN']
    urls_apod = get_astronomy_picture_of_the_day(api_key)
