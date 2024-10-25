import argparse
import json
import os
import requests

from general_functions import download_pictures


def fetch_spacex_last_launch(launch_url):
    response_spacex = requests.get(launch_url)
    response_spacex.raise_for_status()
    data = json.loads(response_spacex.text)
    image_urls = data['links']['flickr']['original']
    for image_number, image_url in enumerate(image_urls):
        image_name = r'images/spacex_{n}.jpg'.format(n=image_number)
        download_pictures(image_url, image_name)


if __name__ == "__main__":
    os.makedirs('images', mode=0o777, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--launch_id', type=str, help='Launch ID of the SpaceX launch', default='latest')
    args = parser.parse_args()

    user_url = f'https://api.spacexdata.com/v5/launches/{args.launch_id}'
    fetch_spacex_last_launch(user_url)
