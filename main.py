#!/usr/bin/env python
"""
Why do people keep photographs?
Every command is launched sequentially from here.
"""


def run():

    from wdpkp import setup
    from wdpkp import requests
    from wdpkp.utils import log
    from wdpkp.movie import image
    from wdpkp.movie import selection
    from wdpkp.movie import ffmpeg
    from wdpkp.movie import text
    from wdpkp.utils import export
    # from wdpkp.movie import subtitles

    # Initialise
    setup.configure()

    log.info('PROGRAM START.')
    log.time('start')

    # Get input
    words = setup.get_words()

    # Make requests and parse responses
    data = requests.get(words)

    log.results(data, 'results-full')

    # Edit the movie
    data = selection.loop(data)

    log.results(data, 'results-selection')

    # adapt images to HD size
    image.resize_images(data)

    # make title & credit screens
    text.title_screen()
    credits_path = text.credit_screen(data)

    # srt file, will be read on movie editing
    # subtitles.create(data)

    # image > movie editing
    video_paths = ffmpeg.edit(data)

    # add the credits and subtitles
    master = ffmpeg.merge(video_paths, credits_path)
    # small = ffmpeg.merge_small(video_paths, credits_path)

    # delete temporary files
    setup.cleanup(data, video_paths, credits_path)

    # copy video to HTTP server
    export.send(master)
    # export.send(small)

    log.info('ALL DONE!')
    log.time('end')


run()
