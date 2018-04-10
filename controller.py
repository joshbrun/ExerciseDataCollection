from YoutubeDownloader.YoutubeDownloader import bulkDownloadVideos
from VideoSplitter.videoSplitter import splitVideos
from JsonProcessing.sortJsonFiles import sortJsonFiles
from JsonProcessing.processJson import processJson
import json
import os

#Does everything

#Download the videos
videos = json.load(open(os.getcwd() + '\data\YoutubeVideos.json'))['Videos']
bulkDownloadVideos(videos)
#
# #Split the videos into frames
splitVideos(videos)
#
# #This requires the bin, include, lib and models in the root dir
os.system("bin\\OpenPoseDemo.exe --image_dir .\\data\\frames --write_images .\\data\\framesOP --write_json .\\data\\json")
#
# #Sort the Json files into directorys
sortJsonFiles()

#Process the Json files into Trainable Normalized vectors
processJson()
