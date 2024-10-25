from datetime import datetime, timedelta
import json
import os
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests

from general_functions import downloading_pictures, file_extension_detection


def earth_polychromatic_imaging_camera(api_key, desired_count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    image_urls = []
    date_today = datetime.now()

    while len(image_urls) < desired_count:
        params = {
            'api_key': api_key,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data:
            if 'image' in item:
                image_url = (f"https://api.nasa.gov/EPIC/archive/natural/{item['date'][:10].replace('-', '/')}"
                             f"/png/{item['image']}.png?api_key={api_key}")
                image_urls.append(image_url)

                if len(image_urls) >= desired_count:
                    break

        date_today = date_today - timedelta(days=1)

    os.makedirs('images', exist_ok=True)

    for image_number, image_url in enumerate(image_urls):
        image_name = f'images/nasa_epic_{image_number}.png'
        try:
            downloading_pictures(image_url, image_name)
        except Exception as e:
            print(f"Error downloading image {image_number}: {e}")

    return image_urls


if __name__ == "__main__":
    api_key = os.environ.get('api_key')
    urls_epic = earth_polychromatic_imaging_camera(api_key)
