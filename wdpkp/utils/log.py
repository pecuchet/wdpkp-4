import json
import logging

from datetime import datetime
from wdpkp import settings


UNDERLINE = '\033[4m'
ENDC = '\033[0m'

time_start = 0


def configure():
    logging.basicConfig(filename=settings.DIR_DATA_DATE + settings.TODAY + '.log',
                        level=logging.DEBUG,
                        filemode='a',
                        format='%(asctime)s:%(levelname)s: %(message)s')


def time(t):
    if t == 'start':
        global time_start
        time_start = datetime.now()
        info('Program start time : ' + str(time_start))
    elif t == 'end':
        info('Program end time : ' + str(datetime.now()))
        info('Program duration : ' + str(datetime.now() - time_start))


def info(msg):
    if settings.DEBUG:
        print(msg)
    logging.info(msg)


def warning(msg):
    if settings.DEBUG:
        print(UNDERLINE + msg + ENDC)
    logging.warning(msg)


def error(msg):
    if settings.DEBUG:
        print(UNDERLINE + msg + ENDC)
    logging.error(msg)


def results(data, name):
    with open(settings.DIR_DATA_DATE + name + '.log', 'wt') as outfile:
        json.dump(data, outfile, indent=4)

