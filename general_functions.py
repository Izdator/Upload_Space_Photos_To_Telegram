import os


import requests


from urllib.parse import urlparse, unquote


def downloading_pictures(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def file_extension_detection(url_extension):
    url_components = urlparse(url_extension)
    path = url_components.path
    filename, ext = os.path.splitext(os.path.basename(path))
    extension = unquote(ext)
    return extension
