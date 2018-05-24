# coding=utf-8

"""
Controller for the pre-processing, and creation of the trainable data sets.
"""

from youtubedownloader.youtubedownloader import bulk_download_videos
from videosplitter.videosplitter import split_videos
from jsonprocessing.sortjsonfiles import sort_json_files
from jsonprocessing.processjson import process_json
from openpose.openPose import run_openpose

from os.path import join
from json import load

# File and directory locations.
DATA_DIR = "data"
VIDEO_FILE = "YoutubeVideos.json"
FRAMES_DIR = "frames"
JSON_DIR = "json"
TRAINING_DIR = "training"

# Paths
video_path = join(DATA_DIR, VIDEO_FILE)
frames_path = join(DATA_DIR, FRAMES_DIR)
json_path = join(DATA_DIR, JSON_DIR)
training_path = join(DATA_DIR, JSON_DIR)

# Sequential Pipeline flow
# Gets the list of videos
videos = load(open(video_path))['Videos']

# Download the videos
bulk_download_videos(videos)

# Split the videos into frames
split_videos(videos)

# This requires the bin, include, lib and models in the root dir
run_openpose(frames_path, json_path)

# Sort the Json files into directories
sort_json_files()

# Process the Json files into Trainable Normalized vectors
process_json(DATA_DIR, training_path)
