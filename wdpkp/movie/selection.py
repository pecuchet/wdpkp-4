import random

from wdpkp import settings
from wdpkp.utils import log
from wdpkp.movie import image


def loop(data):
    """
    Loop over the word data result set from APIs
    :param data:
    :return:
    """
    for idx, word_data in data.items():

        image_data = False

        if 'urls' in word_data:
            if not settings.DEBUG:
                image_data = _get_image(idx, word_data)
            else:
                image_data = _get_image_debug(idx, word_data)

            # remove the full response of the API
            del data[idx]['urls']

        if image_data:
            # image was selected, passed all tests and successfully saved
            # and update the word data with the selected image
            data[idx].update(image_data)
        else:
            # no image was found from url list, or no url list,
            # add black frame
            log.error('No image found in URL list. Adding a black frame.')
            data[idx].update({
                'file': settings.BLACK_FRAME,
                'url': '',
                'type': 'image/png'
            })

    return data


def _get_image(word_idx, word_data):
    """
    Loop over the parsed URL list,
    break when the image was successfully saved
    :param word_idx:
    :param word_data:
    :return:
    """
    for i, url in enumerate(word_data['urls']):

        if settings.URL_BLACKLIST.search(url):
            log.warning('Blacklisted URL, skipping...')
            continue

        downloaded = image.get(url, word_idx)

        if downloaded and image.analyse(downloaded['image']):

            # if analysis passed, save the image
            saved = image.save(downloaded)

            if saved:
                return {
                    'file': saved,
                    'url': url,
                    'type': downloaded['type']
                }

    return None


def _get_image_debug(word_idx, word_data):
    """
    Same as _get_image function, but choose randomly from the list
    :param word_idx:
    :param word_data:
    :return:
    """

    url = random.choice(word_data['urls'])

    downloaded = image.get(url, word_idx)

    if downloaded and image.analyse(downloaded['image']):

        # if analysis passed, save the image
        saved = image.save(downloaded)

        if saved:
            return {
                'file': saved,
                'url': url,
                'type': downloaded['type']
            }
        else:
            return _get_image_debug(word_idx, word_data)
    else:
        return _get_image_debug(word_idx, word_data)
