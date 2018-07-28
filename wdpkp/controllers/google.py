import urllib.parse

import os
from wdpkp import settings

NAME = "google"
ENDPOINT = "https://www.googleapis.com/customsearch/v1"
TEST_DATA = "google.json"

# @see https://developers.google.com/custom-search/json-api/v1/reference/cse/list
# @example request URL
# https://www.googleapis.com/customsearch/v1
#       ?q=Why&cx=xxx&key=xxxx
#       &googlehost=google.com
#       &dateRestrict=d1
#       &start=1&searchType=image
#       &imgType=photo&imgColorType=color
#       &imgSize=xxlarge
#       &safe=off
#       &fields=items(link)


def get_http_headers():
    return {}


def get_url(query):

    if not settings.DEBUG:
        return (ENDPOINT
                + '?q=' + urllib.parse.quote_plus(query)
                + '&cx=' + urllib.parse.quote_plus(os.getenv("GOOGLE_CX"))
                + '&key=' + urllib.parse.quote_plus(os.getenv("GOOGLE_KEY"))
                + '&googlehost=google.com'
                + '&dateRestrict=d1'
                + '&start=1'                    # index of the first result to return
                + "&searchType=image"
                + "&imgType=photo"
                + "&imgColorType=color"         # mono, gray
                + "&imgSize=xxlarge"            # icon, small, medium, large, xlarge, xxlarge, huge
                + "&safe=medium"                # off (default), medium, high
                + "&fields=items(link)")        # partial response, e.g. items(image(byteSize,height,width),link,mime)
    else:
        return settings.DEBUG_BASE_URL + TEST_DATA


def parse(response):
    data = response

    if 'items' in data and len(data['items']) != 0:
        data = data['items']
        urls = []
        for item in data:
            urls.append(item['link'])
        return urls

    return False
