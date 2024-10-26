import os


import requests


from urllib.parse import urlparse, unquote


def download_picture(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def detect_file_extension(url_extension):
    url_components = urlparse(url_extension)
    path = url_components.path
    filename, ext = os.path.splitext(os.path.basename(path))
    extension = unquote(ext)
    return extension
