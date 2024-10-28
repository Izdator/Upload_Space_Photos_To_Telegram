from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
import requests
from general_functions import download_picture


def capture_earth_polychromatic_imaging_camera(api_key, start_date, desired_count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    image_urls = []

    date_today = datetime.strptime(start_date, '%Y-%m-%d')
    target_date = date_today - timedelta(days=desired_count)

    os.makedirs('images', exist_ok=True)

    params = {
        'api_key': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        epic_content = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding the JSON response.")
        return []

    for image_content in epic_content:
        if 'image' in image_content:
            image_date = image_content['date'][:10]  # Получаем дату в формате YYYY-MM-DD
            if image_date == target_date.strftime('%Y-%m-%d'):
                image_base_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date.replace('-', '/')}/png/{image_content['image']}.png"
                image_url = f"{image_base_url}?api_key={params['api_key']}"
                image_urls.append(image_url)
                if len(image_urls) >= desired_count:
                    break

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

    start_date = '2023-09-22'
    desired_days = 10
    urls_epic = capture_earth_polychromatic_imaging_camera(api_key, start_date, desired_count=desired_days)
