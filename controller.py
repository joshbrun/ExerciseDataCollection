from YoutubeDownloader.YoutubeDownloader import bulkDownloadVideos
from VideoSplitter.videoSplitter import splitVideos
import json
import os

#Does everything

#Download the videos
videos = json.load(open(os.getcwd() + '\data\YoutubeVideos.json'))['Videos']
bulkDownloadVideos(videos)

#Split the videos into frames
splitVideos(videos)