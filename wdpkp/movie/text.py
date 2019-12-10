"""
Generate title screen and credits
"""
import os
import textwrap
import subprocess

from urllib import parse as parseURL
from wdpkp import settings
from wdpkp.utils import log
from wdpkp.movie import ffmpeg

credit_speed = 100


def title_screen():
    """
    Write the title on a black background
    @see https://ffmpeg.org/ffmpeg-filters.html#drawtext-1

    ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=0.5 \
        -vf "drawtext=fontsize=30:fontcolor=white:fontfile=/path/font.ttf:text='Title':x=(w-text_w)/2:y=(h-text_h)/2" \
        -frames:v 1 output.png

    :return:
    """
    date = settings.TODAY.split('-')
    date = date[2] + '-' + date[1] + '-' + date[0]
    draw_text = 'drawtext=fontsize=' + str(settings.FONT_SIZE) + ':fontcolor=white:fontfile=\'' + settings.FONT + '\''

    cmd = ffmpeg.get_command()

    cmd += '-f lavfi '
    cmd += '-i color=c=black:s=1920x1080:d=0.5 '
    cmd += '-vf "' + draw_text + ':text=\'' + date + '\':x=(w-text_w)/2:y=((h-text_h)/2)+50" '
    cmd += '-frames:v 1 ' + settings.DIR_DATA_DATE + '0.png'

    os.system(cmd)

    log.info('TITLE SCREEN SAVED.')


def credit_screen(data):
    """
    Build ffmpeg command for the rolling credit screen:
    for each line append a drawtext command
    @see http://stackoverflow.com/questions/11058479/ffmpeg-how-does-moving-overlay-text-command-work

    ffmpeg -y -f lavfi -i color=c=black:s=1920x1080:d=10 \
        -vf drawtext="fontfile='/path/font.ttf':text='Rolling':fontsize=20:fontcolor=white:x=(w-text_w)/2:y=h-20*t" \
        output.mp4

    :return:
    """

    log.info('CREATING ROLLING CREDITS...')

    data = _credit_string_list(data)
    credits_total = len(data)
    count = -1
    duration = 120

    cmd = ffmpeg.get_command()
    cmd += ' -f lavfi -i color=c=black:s=1920x1080:r=24:d=' + str(duration) + ' -vf "'

    draw_txt_cmds = []

    for i in range(0, credits_total):
        count += 1
        credit_sub_lines = []
        for j in range(0, len(data[i])):
            count += 1
            credit_sub_lines.append(_credit_line(count, data[i][j]))

        draw_txt_cmds.append(','.join(credit_sub_lines))

    # append last line after a space
    # 'concept Tessa Groenewoud; code Arnaud Coolsaet'
    draw_txt_cmds.append(_credit_line_last(count))

    # join all the drawtext commands
    cmd += ','.join(draw_txt_cmds) + '" '

    # append output path '{today}/{last-frame-number}.mp4'
    credits_path = settings.DIR_DATA_DATE + 'credits.mp4'

    # lossless H264 export
    cmd += '-an -c:v libx264 -r 24 -preset ultrafast -qp 0 ' + credits_path

    # using unicode in drawtext text
    subprocess.call(cmd.encode('utf8'), shell=True)

    log.info('ROLLING CREDITS SAVED.')

    return credits_path


def _credit_string_list(data):
    """
    Create a list with credit lines of max 62 characters.
    :return:
    """
    credit_list = []

    for i, word_data in data.items():
        # if no url (i.e. a black fallback frame), no need for crediting
        if word_data['url']:
            # Artist's pictures have a specific credit
            if 'assets/tessa/images' not in word_data['url']:
                txt = _drawtext_escape(word_data['url'])
            else:
                txt = "Artist\u2019s archive"
            # wrap the lines
            credit_lines = textwrap.wrap(txt, width=62)
            credit_list.append(credit_lines)

    return credit_list


def _drawtext_escape(url):
    """
    Escaping ffmpeg's filter drawtext escaping madness.
    :param url:
    :return:
    """
    # we have seen single quotes in some urls...
    url = url.replace("'", "")
    url = parseURL.unquote(url)
    url = url.replace(":", "\u003A") \
        .replace("'", "")\
        .replace('"', "")\
        .replace("%", "")\
        .replace(",", "")\
        .replace("[", "")\
        .replace("]", "")\
        .replace(";", "")
    return url


def _get_drawtext_settings():
    """
    Retrieve drawtext layout parameters.
    :return:
    """
    return 'drawtext=fontsize=25:fontcolor=white:fontfile=\'' + settings.FONT + '\''


def _credit_line(i, text):
    """
    FFmpeg drawtext filter, i.e. get font size, color, font file and,
    center horizontally with x=(w-text_w),
    offset and animate vertically with y=(h+({line height}*{line number}))-{animation speed}*t
    :param i:
    :param text:
    :return:
    """
    text = str.replace(text, ':', '\:')
    draw_txt = _get_drawtext_settings()
    # http://www.doubledeclic.com/activites/ISO/iso2010/catalogue/Albums/M/slides/41%20-%20Away%20from%20world%20-%20MITRA%20ARGHYA%20-%20india.jpg
    return draw_txt + ':text=\'' + text + '\':x=(w-text_w)/2:y=(h+(35*' + str(i) + '))-' + str(credit_speed) + '*t'


def _credit_line_last(total_lines):
    """
    Last credits follow the bottom to top animation of
    the previous credits, but stop once at the center of the screen.
    :param total_lines:
    :return:
    """
    txt1 = 'concept'
    txt2 = 'Tessa Groenewoud'
    txt3 = 'code'
    txt4 = 'Arnaud Coolsaet'

    total_offset = str(35*total_lines)

    draw_txt = _get_drawtext_settings()
    draw_txt += ':text=\'' + txt1 + '\':x=(w-text_w)/2:y=((h+h/2+' + total_offset + '+(35*1))-' + str(credit_speed) + '*t)' + _last_anim_conditions(35*-2, total_offset) + ','

    draw_txt += _get_drawtext_settings()
    draw_txt += ':text=\'' + txt2 + '\':x=(w-text_w)/2:y=((h+h/2+' + total_offset + '+(35*2))-' + str(credit_speed) + '*t)' + _last_anim_conditions(35*-1, total_offset) + ','

    draw_txt += _get_drawtext_settings()
    draw_txt += ':text=\'' + txt3 + '\':x=(w-text_w)/2:y=((h+h/2+' + total_offset + '+(35*5))-' + str(credit_speed) + '*t)' + _last_anim_conditions(35*2, total_offset) + ','

    draw_txt += _get_drawtext_settings()
    draw_txt += ':text=\'' + txt4 + '\':x=(w-text_w)/2:y=((h+h/2+' + total_offset + '+(35*6))-' + str(credit_speed) + '*t)' + _last_anim_conditions(35*3, total_offset)

    return draw_txt


def _last_anim_conditions(y_pos, total_offset):
    speed = str(credit_speed)
    animation_y_max = '(h+' + total_offset + '+(35*3))'
    return '*lte(t*' + speed + '\,' + animation_y_max + ') + (h/2+' + str(y_pos) + ')*gt(t*' + speed + '\,' + animation_y_max + ')'

