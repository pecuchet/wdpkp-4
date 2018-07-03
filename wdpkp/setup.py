import os
import re

from wdpkp import settings
from wdpkp.utils import log
from dotenv import load_dotenv


def configure():
    env_path = settings.DIR + '/.env'
    load_dotenv(dotenv_path=env_path)

    os.mkdir(settings.DIR_DATA_DATE)
    os.mkdir(settings.DIR_VIDEO_DATE)

    log.configure()

    settings.URL_BLACKLIST = re.compile(settings.URL_BLACKLIST)

    log.info('PROGRAM CONFIG OK.')


def get_words():
    """
    Split input text with, and without, punctuation
    :return: dict respecting word order from input text
    """
    words = settings.PHRASE.split()
    words_punc = settings.PHRASE_PUNC.split()
    dictionary = {}

    for i, word in enumerate(words):
        dictionary[i] = {
            'word': word,
            'punc': words_punc[i]
        }

    return dictionary


def cleanup(data, video_parts, credits_path):
    """
    Delete temporary files
    :param data:
    :param video_parts:
    :param credits_path:
    :return:
    """
    # delete rescaled images
    # (0.png, the title screen, is kept for archival)
    for i, word_data in data.items():
        if os.path.exists(settings.DIR_DATA_DATE + str(i + 1) + '-out.png'):
            os.remove(settings.DIR_DATA_DATE + str(i + 1) + '-out.png')
        elif os.path.exists(settings.DIR_DATA_DATE + str(i + 1) + '-out.gif'):
            os.remove(settings.DIR_DATA_DATE + str(i + 1) + '-out.gif')

    # delete temporary gif color palette file, if it exists
    if os.path.exists(settings.DIR_DATA_DATE + 'palette.png'):
        os.remove(settings.DIR_DATA_DATE + 'palette.png')

    # delete credits video
    os.remove(credits_path)

    # delete temporary lossless parts
    for part in video_parts:
        os.remove(part)

    log.info('TEMPORARY DATA DELETED.')
