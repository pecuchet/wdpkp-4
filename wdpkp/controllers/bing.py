from urllib import parse as parselib
from wdpkp import settings
from wdpkp.controllers import keys

ENDPOINT_V5 = "https://api.cognitive.microsoft.com/bing/v5.0/images/search"
TEST_DATA_V5 = "bing.json"


def get_http_headers():
    """
    The subscription key that you received when you signed up for this service.
    :return: dict request header
    """
    return {
        'Ocp-Apim-Subscription-Key': keys.BING
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
            + '&safeSearch=Off'                 # is google's default (Moderate, Strict), default: Moderate
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
            url = parselib.parse_qs(item['contentUrl'].split('?')[1])
            urls.append(url['r'][0])

        return urls

    return False
