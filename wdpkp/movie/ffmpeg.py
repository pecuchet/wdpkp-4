import os
import math
import datetime

from collections import OrderedDict

from wdpkp import settings
from wdpkp.utils import log


def get_command():
    """
    Reduce log level when not debugging
    Logging to a file: FFREPORT=file=file/path/name-%t.log:level=16 /root/bin/ffmpeg ...
    :return:
    """
    if settings.DEBUG == 0:
        return '/root/bin/ffmpeg -hide_banner -loglevel quiet '
    else:
        return 'ffmpeg -hide_banner '


def get_time_codes():
    """
    From a text file with dict of image indices as keys and number of frames as values
    :return:
    """
    import ast
    with open(settings.TIME_CODES, 'r') as f:
        s = f.read()
        return ast.literal_eval(s)


def edit(data):
    """
    Divide the data dict in 4 parts;
    send them separately to the encoder.
    The VPS kills too heavy processes.
    :param data:
    :return:
    """
    count = 0
    chunk_size = math.ceil(len(data) / 5)
    chunks = []
    sub_dict = OrderedDict()

    for i, word_data in data.items():
        sub_dict[i] = word_data
        count += 1
        if count > chunk_size or i == (len(data) - 1):
            chunks.append(sub_dict)
            sub_dict = OrderedDict()
            count = 0

    for i, part in enumerate(chunks):
        chunks[i] = _edit_part(part, str(i + 1))

    return chunks


def _edit_part(data, part):
    """
    Our main still image merging function
    :param data:
    :return:
    """
    time_codes = get_time_codes()
    video_path = settings.DIR_VIDEO_DATE + 'wdpkp-' + settings.TODAY + '-part-' + part + '.mp4'
    num_input_streams = len(data.items())

    log.info('START EDITING VIDEO PART ' + part + '...')

    cmd = get_command()

    if part == '1':
        # extract title image stream
        num_input_streams += 1
        cmd += _img_demux(time_codes[0], settings.DIR_DATA_DATE + '0.png')

    for i, word_data in data.items():

        if word_data['type'] != 'image/gif':
            filename = settings.DIR_DATA_DATE + str(i + 1) + '-out.png'
            # extract image stream, for non gif images
            cmd += _img_demux(time_codes[i + 1], filename)
        else:
            filename = settings.DIR_DATA_DATE + str(i + 1) + '-out.gif'
            # extract image stream, for gif images
            cmd += _img_demux_gif(time_codes[i + 1], filename)

    # says: 'stitch all images together and map to one video stream'
    cmd += "-filter_complex 'concat=n=" + str(num_input_streams) + ":v=1[v]' -map '[v]' "

    # lossless H264 encoding
    cmd += "-an -c:v libx264 -preset ultrafast -qp 0 -pix_fmt yuv420p -r 24 " + video_path

    os.system(cmd)

    log.info('VIDEO PART ' + part + ' EDITED & SAVED.')

    return video_path


def _img_demux(num_frames, filename):
    """
    ffmpeg image2 demuxer arguments for extracting separate images into a video file
    :param num_frames:
    :param filename:
    :return:
    """
    seconds = str(int(num_frames) / 24)
    return '-f image2 -loop 1 -thread_queue_size ' + settings.THREAD_QUEUE_SIZE \
           + ' -framerate 24 ' \
           + ' -t ' + seconds \
           + ' -i ' + filename + ' '


def _img_demux_gif(num_frames, filename):
    """
    Animated GIF demuxer
    @see https://ffmpeg.org/ffmpeg-all.html#gif-1
    :param num_frames:
    :param filename:
    :return:
    """
    seconds = str(int(num_frames) / 24)
    return ' -t ' + seconds \
           + ' -ignore_loop 0 ' \
           + ' -i ' + filename + ' '


def merge(video_parts, credits_video):
    """
    Merge video, credit video + 3s of black.

    Previously subtitles were added here through an external .srt file,
    by the sync was perfect (some timings being very short), the subtitles
    are now burnt in each separate image. For the record, previous filter_complex:

    -filter_complex "[0:v][1:v][2:v] concat=n=3:v=1[v0];\
     [v0]subtitles=filename=/subtitles.srt:fontsdir=/path/:force_style=\'FontName=Helvetica Neue\,FontSize=16\'[v1]" \
     -map "[v1]"

    :param video_parts:
    :param credits_video:
    :return:
    """
    time = datetime.datetime.now()
    # subtitle_file = settings.DIR_VIDEO_DATE + 'wdpkp-' + settings.TODAY + '.srt'
    filename = settings.DIR_VIDEO_DATE + 'wdpkp-' + settings.TODAY + '.mp4'

    log.info('MERGING VIDEO PARTS...')

    cmd = get_command()

    # concatenate the video parts
    num_parts = len(video_parts)
    stream_ids = ''
    for i, part in enumerate(video_parts):
        stream_ids += '[' + str(i) + ':v]'
        cmd += ' -i "' + part + '"'

    # add credits + 3s of black
    # add metadata
    stream_ids += '[' + str(num_parts) + ':v][' + str(num_parts + 1) + ':v]'
    cmd += ' -i "' + credits_video + '"' \
           + ' -f lavfi -i "color=c=black:s=1920x1080:r=24:d=3" ' \
           + ' -filter_complex "' + stream_ids + ' concat=n=' + str(num_parts + 2) + ':v=1[v1]"' \
           + ' -map "[v1]"' \
           + ' -metadata title="' + settings.TITLE + '" -metadata year="' + str(time.year) + '"' \
           + ' -metadata author="Tessa Groenewoud" ' \
           + ' -an -pix_fmt yuv420p -r 24 -movflags faststart ' + filename

    # + '[v0]subtitles=filename=' + subtitle_file + ':fontsdir=' \
    # + settings.FONT_DIR + ':force_style=\'FontName=Helvetica Neue\,FontSize=16\'[v1]"' \

    os.system(cmd)

    log.info('MASTER VIDEO SAVED : ' + filename)

    return filename


def merge_small(video_parts, credits_video):
    time = datetime.datetime.now()
    filename = settings.DIR_VIDEO_DATE + 'wdpkp-' + settings.TODAY + '-320x180.mp4'

    log.info('MERGING SMALL VIDEO...')

    cmd = get_command()

    # concatenate the video parts
    num_parts = len(video_parts)
    stream_ids = ''
    scale_filters = ''

    for i, part in enumerate(video_parts):
        scale_filters += '[' + str(i) + ':v]scale=320x180[v' + str(i) + '];'
        stream_ids += '[v' + str(i) + ']'
        cmd += ' -i "' + part + '"'

    # add credits + 3s of black
    # add metadata
    scale_filters += '[' + str(num_parts) + ':v]scale=320x180[v' + str(num_parts) + '];'
    stream_ids += '[v' + str(num_parts) + ']'
    stream_ids += '[' + str(num_parts + 1) + ':v]'
    cmd += ' -i "' + credits_video + '"' \
           + ' -f lavfi -i "color=c=black:s=320x180:r=24:d=3" ' \
           + ' -filter_complex "' + scale_filters + stream_ids + 'concat=n=' + str(num_parts + 2) + ':v=1[v1]"' \
           + ' -map "[v1]"' \
           + ' -metadata title="' + settings.TITLE + '" -metadata year="' + str(time.year) + '"' \
           + ' -metadata author="Tessa Groenewoud" ' \
           + ' -an -pix_fmt yuv420p -r 24 -crf 18 -movflags faststart ' + filename

    os.system(cmd)

    log.info('SMALL VIDEO SAVED : ' + filename)

    return filename
