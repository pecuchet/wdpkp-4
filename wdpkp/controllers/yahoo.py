import time

import oauth2 as oauth
import urllib.parse

import os
from wdpkp import settings

# @see universal api args : https://developer.yahoo.com/boss/search/boss_api_guide/api_spec.html
# @see image service : https://developer.yahoo.com/boss/search/boss_api_guide/image.html
# can set location through 'market' parameter

# oauth1 implementation
# @see https://github.com/constituentvoice/YahooBoss-Python/blob/master/yahooboss/__init__.py

# @example request URL
# https://yboss.yahooapis.com/ysearch/images
#       ?filter=no
#       &oauth_version=1.0
#       &count=40
#       &oauth_nonce=xxx
#       &dimensions=widewallpaper
#       &oauth_timestamp=1472392829
#       &q=Why
#       &oauth_body_hash=xxx
#       &oauth_consumer_key=xxx
#       &oauth_signature_method=HMAC-SHA1
#       &format=json


NAME = "yahoo"
ENDPOINT = "https://yboss.yahooapis.com/ysearch/images"
TEST_DATA = "yahoo.json"


def get_http_headers():
    return {}


def get_args(query):
    return {
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_version': '1.0',

        'q': urllib.parse.quote_plus(query),
        'filter': 'no',                     # yes (default), in google : default = off
        'count': str(settings.NUM_RESULTS),
        'format': 'json',
        'dimensions': 'widewallpaper'       # all(default), small, medium, large, wallpaper, widewallpaper
    }


def get_url(query):

    if not settings.DEBUG:
        param = get_args(query)
        consumer = oauth.Consumer(key=os.getenv("YAHOO_KEY"), secret=os.getenv("YAHOO_SECRET"))
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req = oauth.Request(method="GET", url=ENDPOINT, parameters=param)
        req.sign_request(signature_method, consumer, None)
        return req.to_url()

    else:
        return settings.DEBUG_BASE_URL + TEST_DATA


def parse(response):
    data = response
    has_keys = 'bossresponse' in data and 'responsecode' in data['bossresponse']

    if has_keys and data['bossresponse']['responsecode'] == '200':
        data = data['bossresponse']['images']['results']
        urls = []
        for item in data:
            urls.append(item['clickurl'])
        return urls

    return False
