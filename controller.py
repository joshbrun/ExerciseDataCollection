# coding=utf-8

"""
Controller for the pre-processing, and creation of the trainable data sets.
"""

from youtubedownloader.youtubedownloader import bulk_download_videos
from videosplitter.videosplitter import split_videos
from jsonprocessing.sortjsonfiles import sort_json_files
from jsonprocessing.processjson import process_json
from openpose.openPose import run_openpose
import os

import json

# File and directory locations.
data_dir = "data"
videos_file = os.path.join(data_dir, "YoutubeVideos.json")
openpose_input = os.path.join(data_dir, "frames")
openpose_output = os.path.join(data_dir, "json")
training_dir = os.path.join(data_dir, "training")

# Gets the list of videos
# videos = json.load(open(videos_file))['Videos']

# Download the videos
# bulk_download_videos(videos)

# Split the videos into frames
# split_videos(videos)

# This requires the bin, include, lib and models in the root dir
# run_openpose(openpose_input, openpose_output)

# Sort the Json files into directories
# sort_json_files()

# Process the Json files into Trainable Normalized vectors
process_json(data_dir, training_dir)
