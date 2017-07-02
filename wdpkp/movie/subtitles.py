import math

import wdpkp.settings as settings
from wdpkp.movie import ffmpeg


def create(data):
    """
    Create a WebVTT file, which will be loaded by the HTML5 video player.
    :param data:
    :return:
    """

    time_codes = ffmpeg.get_time_codes()
    frame_start = time_codes[0]
    frame_end = time_codes[0]

    txt = '\n1\n'
    txt += '00:00:00.000 --> ' + str(_convert_frames_to_ms(frame_end)) + '\n\n'

    for i, word_data in data.items():
        frame_end += time_codes[i+1]

        txt += str(i+2) + '\n'
        txt += str(_convert_frames_to_ms(frame_start)) + ' --> ' + str(_convert_frames_to_ms(frame_end)) + '\n'
        txt += word_data['punc'] + '\n\n'

        frame_start = frame_end

    with open(settings.DIR_VIDEO_DATE + 'wdpkp-' + settings.TODAY + '.srt', 'wt') as out:
        print(txt, file=out)


def _convert_frames_to_ms(frames):
    seconds = frames / 24
    seconds_rounded = math.floor(seconds)
    seconds_padded = '{0:02d}'.format(seconds_rounded)
    milliseconds = (seconds-seconds_rounded) * 1000
    milliseconds_rounded = math.floor(milliseconds)
    milliseconds_padded = '{0:03d}'.format(milliseconds_rounded)
    return '00:00:' + str(seconds_padded) + ',' + str(milliseconds_padded)
