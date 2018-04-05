#Nethan do this.
import json
import os

def downloadVideo(url, name):
    '''
    :param url: The url of the YouTube video.
    :param name: The name of the file to save the YouTube video.
    :return: None
    '''
    print("downloading %s from %s"%(name, url))

def bulkDownloadVideos(videos):
    '''
    :param videos: The array of videos to download
    :return:
    '''
    # Read the json videos file
    print("Videos count: %d" % (len(videos)))
    for video in videos:
        url = video['url']
        label = video['label']
        exercise = video['exercise']
        sex = video['sex']
        view = video['view']
        filename = "%s_%s_%s_%s.mp4" % (label, exercise, sex, view)
        downloadVideo(url, filename)





