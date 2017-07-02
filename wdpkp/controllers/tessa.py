"""
For certain words (why, do, keep, up, to, a, and, I, as, of, in)
handpicked images by the artist may be requested.
"""
from random import shuffle
from wdpkp.controllers import keys


def get_http_headers():
    return {}


def get_url(query):
    return keys.TESSA_DATA_URL


def parse(response):
    """
    Trim out the URLs
    :param response:
    :return:
    """
    if response:
        shuffle(response)
        urls = []
        for item in response:
            urls.append(item['url'])
        return urls
    return False
