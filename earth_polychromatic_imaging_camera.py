from datetime import datetime, timedelta
import json
import os
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests

from general_functions import download_pictures, detect_file_extension


def capture_earth_polychromatic_imaging_camera(api_key, desired_count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    image_urls = []
    date_today = datetime.now()

    while len(image_urls) < desired_count:
        params = {
            'api_key': api_key,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        epic_data = response.json()

        for item in epic_data:
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
            download_pictures(image_url, image_name)
        except requests.exceptions.RequestException as req_err:
            print(f"Request error while downloading image {image_number}: {req_err}")
        except IOError as io_err:
            print(f"I/O error while saving image {image_number}: {io_err}")
        except Exception as e:
            print(f"Unexpected error while downloading image {image_number}: {e}")

    return image_urls


if __name__ == "__main__":
    api_key = os.environ.get('NASA_TOKEN')
    urls_epic = capture_earth_polychromatic_imaging_camera(api_key)
