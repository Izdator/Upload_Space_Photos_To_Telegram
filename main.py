import os


import requests


import json


from urllib.parse import urlparse, unquote


from datetime import datetime, timedelta


from dotenv import load_dotenv


load_dotenv()



api_key = os.environ['api_key']



# def downloading_pictures(url, path):
#     response = requests.get(url)
#     response.raise_for_status()
#     with open(path, 'wb') as file:
#         file.write(response.content)


# os.makedirs('images', mode=0o777, exist_ok=False)

# url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
# filename = 'images/hubble.jpeg'

# downloading_pictures(url, filename)


# def fetch_spacex_last_launch(launch_url):
#     response_spacex = requests.get(launch_url)
#     response_spacex.raise_for_status()
#     data = json.loads(response_spacex.text)
#     image_urls = [link for link in data['links']['flickr']['original']]
#     for image_number, image_url in enumerate(image_urls):
#         image_name =         r'images/spacex_{n}.jpg'.format(n=image_number)
#         response_image = requests.get(image_url)
#         response_image.raise_for_status()
#         with open(image_name, 'wb') as file:
#             file.write(response_image.content)


def file_extension_detection(test_url):
    url_components = urlparse(test_url)
    print(url_components)
    path = url_components.path
    print("Path:", path)
    filename, ext = os.path.splitext(os.path.basename(path))
    print("Filename:", filename)
    print("Extension:", ext)
    extension = unquote(ext)
    print("Decoded Extension:", extension)
    return extension


def astronomy_picture_of_the_day(api_key, count=30):
    base_url = "https://api.nasa.gov/planetary/apod"
    image_urls = []
    date_today = datetime.now()

    for _ in range(count):
        params = {
            'api_key': api_key,
            'date': date_today.strftime('%Y-%m-%d'),
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'url' in data:
            image_urls.append(data['url'])

        date_today = date_today - timedelta(days=1)
    for image_number, image_url in enumerate(image_urls):
        image_name =         r'images/nasa_apod_{n}.jpg'.format(n=image_number)
        response_image = requests.get(image_url)
        response_image.raise_for_status()
        with open(image_name, 'wb') as file:
            file.write(response_image.content)

    return image_urls


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
                image_url = f"https://api.nasa.gov/EPIC/archive/natural/{item['date'][:10].replace('-', '/')}/png/{item['image']}.png?api_key={api_key}"
                image_urls.append(image_url)

                if len(image_urls) >= desired_count:
                    break

        date_today = date_today - timedelta(days=1)

    os.makedirs('images', mode=0o777, exist_ok=True)

    for image_number, image_url in enumerate(image_urls):
        image_name = f'images/nasa_epic_{image_number}.png'
        response_image = requests.get(image_url)
        response_image.raise_for_status()
        with open(image_name, 'wb') as file:
            file.write(response_image.content)

    return image_urls


os.makedirs('images', mode=0o777, exist_ok=True)
# urls_apod = astronomy_picture_of_the_day(api_key)
# print(urls_apod)
urls_epic = earth_polychromatic_imaging_camera(api_key)
print(urls_epic)


print(os.environ['api_key'])



# test_url = "https://example.com/txt/hello%20world.txt?v=9#python"
# file_extension_detection(test_url)


# os.makedirs('images', mode=0o777, exist_ok=False)

# url_spacex_id = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
# fetch_spacex_last_launch(url_spacex_id)
