from datetime import datetime, timedelta
import json
import os
import requests
from dotenv import load_dotenv
from general_functions import download_picture, detect_file_extension


def get_astronomy_picture_of_the_day(api_key, days=1):
    base_url = "https://api.nasa.gov/planetary/apod"
    image_urls = []

    os.makedirs('images', exist_ok=True)

    date_query = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    params = {
        'api_key': api_key,
        'date': date_query,
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    apod_content = response.json()

    if 'url' in apod_content:
        image_urls.append(apod_content['url'])
        image_extension = detect_file_extension(apod_content['url'])
        image_name = f'images/nasa_apod_{date_query.replace("-", "")}{image_extension}'

        try:
            download_picture(apod_content['url'], image_name)
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"Error downloading image from {apod_content['url']}: {e}")

    return image_urls


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ['NASA_TOKEN']

    days_to_fetch = 30
    urls_apod = get_astronomy_picture_of_the_day(api_key, days=days_to_fetch)
