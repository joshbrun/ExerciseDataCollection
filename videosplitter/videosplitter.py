# coding=utf-8

"""
Splits videos into video clips, and then splits th video clips into images.
"""

from os import system, getcwd, name
from os.path import join
import sys
import os

sys.path.append(join(getcwd(), "utilities"))
from utilities.fileutilities import check_directory


def split_videos(videos):
    """

    :param videos:
    """
    print("\n")
    # For each video in videos

    count = 0
    for video in videos:
        for _ in video['parts']:
            count += 1

    print("Extracting frames from", count, " Clips")

    for video in videos:
        for part in video['parts']:
            start_time = round(float(part['startTime']), 3)
            end_time = round(float(part['endTime']), 3)
            duration = end_time - start_time

            input_name = "data/videos/" + video['identifier'] + ".mkv"
            output_dir = "data/frames/"
            file_name = part['label'] + "_" + video['exercise'] + "_" + video['sex'] + "_" + part['view'] + "_" + part[
                'name'] + "_" + video['identifier'] + "_" + "%05d.jpg"
            output = output_dir + file_name

            check_directory("data/frames")
            check_directory("data/framesOP")
            check_directory("data/json")

            if os.name == "posix":
                command = "ffmpeg"
            else:
                command = "ffmpeg.exe"
            command += " -loglevel panic -ss " + part['startTime'] + " -t 00:00:" + str(
                duration) + " -i " + input_name + " " + output + " -hide_banner"
            system(command)
    print("Finished extracting frames from", count, "clips\n")


def get_seconds(time):
    """
    :param time:
    :return:
    """
    h, m, s = time.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
