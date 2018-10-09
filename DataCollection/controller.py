# coding=utf-8

"""
Controller for the pre-processing, and creation of the trainable data sets.
"""

from youtubedownloader.youtubedownloader import bulk_download_videos
from videosplitter.videosplitter import split_videos
from jsonprocessing.sortjsonfiles import sort_json_files
from jsonprocessing.processjson import process_json
# from jsonprocessing.sequenceprocessjson import process_json
# from openpose.openPose import run_openpose
from openposeC.openPose import run_openpose

from os.path import join
from json import load

# File and directory locations.
DATA_DIR = "data"
VIDEO_FILE = "YoutubeVideos"
TRAINING_MODIFIER = "_training"
VALIDATION_MODIFIER = "_validation"
TESTING_MODIFIER = "_testing"
VIDEO_DIR = "videos"
FRAMES_DIR = "frames"
JSON_DIR = "json"
OUTPUT_DIR = "output"
MODIFIERS = [TRAINING_MODIFIER, VALIDATION_MODIFIER, TESTING_MODIFIER]

for modifier in MODIFIERS:
    # Paths
    videos = join(DATA_DIR, VIDEO_FILE + modifier)
    videos_path = join(DATA_DIR, VIDEO_DIR + modifier)
    frames_path = join(DATA_DIR, FRAMES_DIR + modifier)
    json_path = join(DATA_DIR, JSON_DIR + modifier)
    output_path = join(DATA_DIR, OUTPUT_DIR + modifier)

    # Sequential Pipeline flow
    # Gets the list of videos
    videos = load(open(videos))['Videos']

    # Download the videos
    bulk_download_videos(videos, videos_path)

    # Split the videos into frames
    split_videos(videos, videos_path, frames_path)

    # This requires the bin, include, lib and models in the root dir
    run_openpose(frames_path, json_path, 4)

    # Sort the Json files into directories
    sort_json_files(json_path)

    # Process the Json files into Trainable Normalized vectors
    process_json(json_path, output_path)
