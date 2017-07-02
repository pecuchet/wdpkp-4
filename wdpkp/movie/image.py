import subprocess
import urllib.request

from wdpkp import settings
from wdpkp.utils import log
from wdpkp.movie import ffmpeg


def get(url, word_idx):
    """
    using urlopen to avoid download errors and get content-type
    although APIs return image types
    without checking for HTTP errors, one could use 'urllib.request.urlretrieve(url, path)'
    :param url:
    :param word_idx:
    :return:
    """
    try:
        log.info('Requesting image: ' + str(word_idx + 1))
        req = urllib.request.urlopen(url)
    except urllib.request.URLError as e:
        log.warning('Image request failed ' + str(e.reason) + ' ' + url)
        return False

    content_type = req.info()['Content-Type']
    extension = get_extension(content_type)

    if extension:
        return {
            'name': word_idx + 1,
            'image': req,
            'extension': extension,
            'type': content_type
        }

    return False


def analyse(downloaded):
    return True


def save(downloaded):
    """
    Saves image as 'idx.ext' based on HTTP Content-Type
    :param downloaded:
    :return:
    """
    log.info('Saving image: ' + str(downloaded['name']) + downloaded['extension'])
    path = settings.DIR_DATA_DATE + str(downloaded['name']) + downloaded['extension']
    with open(path, 'wb') as output:
        output.write(downloaded['image'].read())
    return path


def get_extension(mime):
    """
    Extension based on the server's content-type.
    :param mime:
    :return:
    """
    if mime == 'image/jpeg':
        return '.jpg'
    if mime == 'image/png':
        return '.png'
    if mime == 'image/gif':
        return '.gif'
    if mime == 'image/tiff':
        return '.tif'
    return False


def _resize_gif_cmd(input_name):
    """
    Animated GIF muxer.
    Optimizing quality by creating a palette before resizing.
    @see https://www.ffmpeg.org/ffmpeg-formats.html#gif-2
    @see http://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
    @see http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html

    ffmpeg -y -i anim.gif -vf fps=24,palettegen palette.png
    ffmpeg -i anim.gif -i palette.png -filter_complex "fps=24, scale=...[x];[x][1:v]paletteuse" out.gif

    :param input_name:
    :return:
    """
    palette_png = settings.DIR_DATA_DATE + 'palette.png'

    # generate a palette from the input, overwrite it by default (-y)
    cmd = ffmpeg.get_command() \
          + '-y -i "' + input_name + '" -vf fps=24,palettegen ' + palette_png + ';'

    # rescale and pad gif using saved palette.png
    cmd += ffmpeg.get_command() \
           + ' -i ' + input_name \
           + ' -i ' + palette_png \
           + ' -filter_complex "fps=24,' + _get_scale_args() + '[x];[x][1:v]paletteuse[v0];' \

    return cmd


def _get_scale_args():
    """
    Scale and padding algorithm.
    :return:
    """
    w = str(settings.WIDTH)
    h = str(settings.HEIGHT)

    scale = 'scale=iw*min(' + w + '/iw\,' + h + '/ih):ih*min(' + w + '/iw\,' + h + '/ih),'
    pad = 'pad=' + w + ':' + h + ':(' + w + '-iw*min(' + w + '/iw\,' + h + '/ih))/2:(' + h + '-ih*min(' + w + '/iw\,' + h + '/ih))/2:0x000000,'
    sar_dar = 'setsar=1/1,setdar=16/9'

    return scale + pad + sar_dar


def resize_images(data):
    """
    Resize and fit each image in a HD frame, by padding it with black where necessary,
    this makes the subsequent ffmpeg command to create the full video much simpler.
    The subtitle text is also burned in here per image (keeping the sync between image and
    text perfect. Because some pictures have very short timings, ffmpeg couldn't synchronize
    perfectly using a subtitle file, which was merged on the full video.)

    Several quality tests were done, jpg had color space issues (black wasn't black),
    tiff is quite heavy to process... function uses png, below are the test commands:

    ## png > +/- 3.1MB
    ffmpeg -i in.jpg -filter:v "scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), \
        pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2:black, \
        setsar=1/1, setdar=16/9" \
        out.png

    ## jpg > quality -q:v 1 (max) - 31 (min) > padded black is not 100% black
    ffmpeg -i in.jpg -filter:v "scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih), \
        pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2:0x000000, \
        setsar=1/1, setdar=16/9" \
        -q:v 1 -pix_fmt yuvj420p out.jpg

    ## jpg > better
    ffmpeg -f lavfi -i color=c=black:s=1920x1080 -i in.jpg \
        -filter_complex "[1:v]scale=..., setsar=1/1, setdar=16/9[ovr];[ovr]blend=all_mode='normal'[v]" \
        -map '[v]' -q:v 1 -pix_fmt yuvj420p out.jpg

    ## tiff > best > +/- 6MB
    ffmpeg -i in.jpg -filter:v "scale=..., setsar=1/1, setdar=16/9" -compression_algo raw -pix_fmt rgb24 out.tiff
    @see http://superuser.com/questions/881783/convert-from-avi-to-uncompressed-tiff-using-ffmpeg

    :param data:
    :return:
    """
    draw_text = 'drawtext=fontsize=40:fontcolor=white:borderw=2:fontfile=\'' + settings.FONT_BOLD + '\''
    cmd = ''

    log.info('RESCALING IMAGES...')

    for i, word_data in data.items():

        if word_data['type'] == 'image/gif':
            # save as gif
            filename = settings.DIR_DATA_DATE + str(i + 1) + '-out.gif'
            cmd += _resize_gif_cmd(word_data['file']) \
                + '[v0]' + draw_text + ':text=\'' + word_data['punc'] + '\':x=(w-text_w)/2:y=(h-110)[v1]"' \
                + ' -map "[v1]" -pix_fmt rgb8 ' + filename + ';'

        else:
            # save as png
            filename = settings.DIR_DATA_DATE + str(i + 1) + '-out.png'
            cmd += ffmpeg.get_command() \
                   + ' -i ' + word_data['file'] \
                   + ' -filter_complex "' + _get_scale_args() + '[v0];' \
                   + '[v0]' + draw_text + ':text=\'' + word_data['punc'] + '\':x=(w-text_w)/2:y=(h-110)[v1]"' \
                   + ' -map "[v1]" -pix_fmt rgb24 ' + filename + ';'

        # store tmp path
        data[i].update({'tmp': filename})

    # run all rescaling commands at once
    subprocess.call(cmd.encode('utf8'), shell=True)

    log.info('IMAGES RESCALED.')
