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

        #Split the downloaded file into the required parts using something like

        #ffmpeg - ss(starttime) -t(duration) -c: v copy - c: a copy(title.mp4)
        #Could be done somewhere else 
        #So we can extract the frames directly from the part clips,
        #Instead of having to extract all the frames then approximating the frames from time and frames count






