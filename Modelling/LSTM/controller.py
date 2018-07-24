# coding=utf-8

"""
Controller for the pre-processing, and creation of the trainable data sets.
"""
from sequenceprocessjson import process_json

from os.path import join
from json import load

# File and directory locations.
DATA_DIR = "data"
VIDEO_FILE = "YoutubeVideos"
TRAINING_MODIFIER = "_training"
VALIDATION_MODIFIER = "_validation"
VIDEO_DIR = "videos"
FRAMES_DIR = "frames"
JSON_DIR = "json"
OUTPUT_DIR = "output"
MODIFIERS = [TRAINING_MODIFIER, VALIDATION_MODIFIER]

for modifier in MODIFIERS:
    # Paths
    videos = join(DATA_DIR, VIDEO_FILE + modifier)
    videos_path = join(DATA_DIR, VIDEO_DIR + modifier)
    frames_path = join(DATA_DIR, FRAMES_DIR + modifier)
    json_path = join(DATA_DIR, JSON_DIR + modifier)
    output_path = join(DATA_DIR, OUTPUT_DIR + modifier)

    # Process the Json files into Trainable Normalized vectors
    process_json(json_path, output_path)
