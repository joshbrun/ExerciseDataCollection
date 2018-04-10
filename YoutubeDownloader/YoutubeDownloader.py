import json
import os
import youtube_dl


def downloadVideo(identifier):
    """
    :param identifier: The identifier of the YouTube video.
    :return: None
    """
    print("downloading %s" % (identifier))
    ydl_opts = {
        'outtmpl': 'data/videos/' + identifier,
        'dump_single_json': 'true',
        'merge_output_format': 'mkv'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([identifier])
        #ydl.prepare_filename(ydl.extract_info("{}".format(identifier)))

def bulkDownloadVideos(videos):
    """
    :param videos: The array of videos to download
    :return:
    """
    # Read the json videos file
    print("Videos count: %d" % (len(videos)))
    for video in videos:
        identifier = video['identifier']
        filename = "%s.mkv" % (identifier)
        downloadVideo(identifier)
