# coding=utf-8

"""
processjson.js converts multiple openpose Frames into trainable data sets.
Author: Joshua Brundan, Nathan Henderson
"""

from os import getcwd, listdir
import json
from os.path import join, isfile
import sys

sys.path.append(join(getcwd(), "utilities"))
from utilities.fileutilities import check_directory


def calculate_hcs(filename, label):
    """
    :param filename:
    :param label:
    :return:
    """
    # print("Calculating Gradients for filename: "+filename+", label: "+label);
    correctness = 0
    if label == "true":
        correctness = 1

    line = ""
    file = open(filename, 'r')
    lines = file.readline()
    people = json.loads(lines)['people']

    # If there are more than one person in the frame only use the first.
    key_points = people[0]['pose_keypoints_2d']

    right_hip_x = key_points[8 * 3]
    right_hip_y = key_points[8 * 3 + 1]

    # normalise around the right hip
    for i in range(0, len(key_points)):
        a=3
        # if i % 3 == 0:
        #     key_points[i] -= right_hip_x
        # if i % 3 == 1:
        #     key_points[i] -= right_hip_y
    line = ",".join(map(str, key_points))
    line += "," + str(correctness)

    file.close()

    return line

def process_json(input_dir: str, output_dir: str) -> None:
    """
    Processes the Json files into trainable data sets.
    :param input_dir: The location of the Json data.
    :param output_dir: The location of the Training directory.
    """
    print("\nConverting the separate Json files into a Trainable Vector Set")
    check_directory(output_dir)
    check_directory(input_dir)

    # Read the sets
    file_name = "exerciseList"
    file = open(join("data", file_name), 'r')
    sets = []

    for line in file.readlines():
        if not line[:-2] in sets:
            sets.append(line[:-2])
    file.close()

    print("Sets to process: %d" % (len(sets)))

    json_dir = input_dir #join(input_dir, "json")

    for data_set in sets:
        set_name_list = data_set.split("/")

        agg_output_file_name = set_name_list[1] + "_" + set_name_list[3]
        output_agg_file = open(output_dir + "/" + agg_output_file_name + ".csv", "a")

        for label in ["true", "false"]:
            set_dir = json_dir + "/" + label + "/" + data_set
            print("c")
            try:
                files = [f for f in listdir(set_dir) if isfile(join(set_dir, f))]
                print("a")
                files.sort()
                lines = []
                for json_file in files:
                    print("b")
                    lines.append(calculate_hcs(set_dir + "/" + json_file, label))

                # for line in lines:
                #     if not (line == "[]"):
                #         output_agg_file.write(line + "\n")

            except FileNotFoundError as e:
                print(e)
                continue

        # output_file.close()
    print("Sets Processed")