#!/usr/bin/env python
"""
Check if the video was generated,
if not launch the process again.
"""
import os
import shutil
import datetime


def check():
    today = datetime.datetime.now().isoformat().split('T')[0]
    wdpkp_dir = os.path.dirname(os.path.realpath(__file__))
    video_dir = wdpkp_dir + '/videos/' + today

    if not os.path.isdir(video_dir) or not os.path.exists(video_dir + '/wdpkp-' + today + '.mp4'):
        # remove today's data_tmp if present
        if os.path.isdir(wdpkp_dir + '/data_tmp/' + today):
            shutil.rmtree(wdpkp_dir + '/data_tmp/' + today)
        # remove today's video dir if present
        if os.path.isdir(video_dir):
            shutil.rmtree(video_dir)
        import main
        return

check()
