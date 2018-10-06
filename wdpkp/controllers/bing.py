# from urllib import parse as parselib

import os
from wdpkp import settings

ENDPOINT_V5 = "https://api.cognitive.microsoft.com/bing/v5.0/images/search"
TEST_DATA_V5 = "bing.json"


def get_http_headers():
    """
    The subscription key that you received when you signed up for this service.
    :return: dict request header
    """
    return {
        'Ocp-Apim-Subscription-Key': os.getenv("BING")
    }


def get_url(query):
    """
    Build the request url
    :param query:
    :return: string URL
    """
    if settings.DEBUG:
        return settings.DEBUG_BASE_URL + TEST_DATA_V5

    return (ENDPOINT_V5
            + '?count=' + str(settings.NUM_RESULTS)
            + '&q=' + query
            + '&aspect=All'                     # Square, Wide, Tall, All
            + '&color=ColorOnly'                # Monochrome
            # + '&freshness=Day'                # Bing is very strict, loosen it
            + '&safeSearch=Moderate'            # is google's default (Moderate, Strict), default: Moderate
            + '&imageType=Photo'
            # + '&modulesRequested=Annotations' # Collections (a list of related images)
                                                # Annotations (characteristics of the type of content found)
                                                # Caption (provides information about the image)
                                                # RecognizedEntities (list of entities (people) that were recognized)
            + '&size=Wallpaper')                # Large <= 500x500


def parse(response):
    """
    Trim out the URLs
    :param response:
    :return:
    """
    data = response

    if 'value' in data and len(data['value']):
        urls = []

        for item in data['value']:
            urls.append(item['contentUrl'])
            # Microsoft seems to have changed the format of the 'contentUrl' value
            # before 14/09/2018 this was bing.com url with the image url encoded as a query parameter
            # from 14/09 it returned the non-encoded image url
            # url = parselib.parse_qs(item['contentUrl'].split('?')[0])
            # urls.append(url['r'][0])

        return urls

    return False
