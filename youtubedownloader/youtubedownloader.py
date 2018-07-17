# coding=utf-8

"""
Handles the downloading of youtube videos in bulk.
Author: Joshua Brundan, Nathan Henderson.
"""

import youtube_dl
from os.path import join


def download_video(identifier, path):
    """
    :param identifier: The identifier of the YouTube video.
    :return: None
    """
    print("downloading %s" % identifier)
    ydl_opts = {
        'outtmpl': join(path, identifier),
        'dump_single_json': False,
        'merge_output_format': 'mkv'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try :
            ydl.download([identifier])
        except:
            print("Error downloading: ", identifier)
        # ydl.prepare_filename(ydl.extract_info("{}".format(identifier)))


def bulk_download_videos(videos, path):
    """
    :param videos: The array of videos to download
    :return:
    """
    # Read the json videos file
    print("Videos count: %d" % (len(videos)))
    for video in videos:
        identifier = video['identifier']
        # filename = "%s.mkv" % identifier
        if video['local'] == "false":
            download_video(identifier, path)
