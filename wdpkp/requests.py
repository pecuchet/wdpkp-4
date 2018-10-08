import json
import random
import urllib.request
import importlib

from wdpkp import settings
from wdpkp.utils import log

# 'wdpkp.controllers.yahoo', yahoo BOSS API is out of service as of 15/05/2018

controllers = list(
    map(importlib.import_module,
        ['wdpkp.controllers.bing', 'wdpkp.controllers.google', 'wdpkp.controllers.tessa'])
)

times_relaunched = 0

artists_words = ['why', 'do', 'keep', 'up', 'to', 'a', 'and', 'I', 'as', 'of', 'in']
artists_count = 0


def _make_request(url, headers):
    """
    Handle API requests and errors
    :param url:
    :param headers:
    :return:
    """
    log.info('FETCHING: ' + url)
    req = urllib.request.Request(url, None, headers)

    try:
        req = urllib.request.urlopen(req)
        encoding = req.info().get_content_charset('utf-8')
        data = req.read()
        return json.loads(data.decode(encoding))
    except urllib.request.URLError as e:
        log.warning('REQUEST FAILED: ' + str(e.reason))
        return False


def _choose_controller(word):
    """
    Randomly choose a controller,
    for certain words the extra controller 'tessa' may be used max 2 times.
    :param word:
    :return:
    """
    global artists_words, artists_count

    # default is not to use the last controller
    rand_max = len(controllers) - 2

    # allow to use the last controller
    if artists_count < 2 and (word in artists_words):
        rand_max = rand_max + 1

    # random between 0-1 or 0-2
    controller_id = random.randint(0, rand_max)

    if controller_id is 2:
        artists_count += 1

    return controllers[controller_id]


def get(words):
    """
    Call APIs synchronously,
    re-invoke the method if requests failed
    :param words:
    :return:
    """
    global times_relaunched
    failed = 0

    for i, val in words.items():

        # only continue for previously failed requests
        if 'api' in words[i]:
            continue

        # choose a controller
        controller = _choose_controller(val['word'])

        # construct the URL param
        url = controller.get_url(val['word'])
        headers = controller.get_http_headers()

        # make the request
        response = _make_request(url, headers)

        # handle response
        if response:
            controller_name = controller.__name__.split('.')[-1]
            # get the returned image URLs
            parsed = controller.parse(response)
            if parsed:
                words[i]['api'] = controller_name
                words[i]['urls'] = parsed
            else:
                log.warning('Nothing parsed from ' + controller_name)
                failed = 1
        else:
            # failed HTTP requests are logged above
            failed = 1

    # re-request for failed responses
    if failed and settings.ALLOW_RELAUNCH and settings.RELAUNCH_TIMES >= times_relaunched:
        times_relaunched += 1
        log.info('Relaunching failed requests...')
        get(words)

    return words
