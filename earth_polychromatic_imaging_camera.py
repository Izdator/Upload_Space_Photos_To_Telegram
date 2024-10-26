from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
import requests

from general_functions import download_picture


def capture_earth_polychromatic_imaging_camera(api_key, desired_count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    image_urls = []
    date_today = datetime.now()

    while len(image_urls) < desired_count:
        params = {
            'api_key': api_key,
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            epic_content = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            break
        except json.JSONDecodeError:
            print("Error decoding the JSON response.")
            break

        for image_content in epic_content:
            if 'image' in image_content:
                image_base_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_content['date'][:10].replace('-', '/')}/png/{image_content['image']}.png"

                image_url = f"{image_base_url}/api_key={params['api_key']}"
                image_urls.append(image_url)

                if len(image_urls) >= desired_count:
                    break

        date_today = date_today - timedelta(days=1)

    os.makedirs('images', exist_ok=True)

    for image_number, image_url in enumerate(image_urls):
        image_name = f'images/nasa_epic_{image_number}.png'
        try:
            download_picture(image_url, image_name)
        except requests.exceptions.RequestException as req_err:
            print(f"Request error while downloading image {image_number}: {req_err}")
        except IOError as io_err:
            print(f"I/O error while saving image {image_number}: {io_err}")

    return image_urls


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get('NASA_TOKEN')
    if not api_key:
        raise ValueError("API key is missing or invalid.")
    urls_epic = capture_earth_polychromatic_imaging_camera(api_key)
