# coding=utf-8

"""
processjson.js converts multiple openpose Frames into trainable data sets.
Author: Joshua Brundan, Nathan Henderson
"""

import os
import json
import sys

PART_MAPPING = {
    0: "Nose",
    1: "Neck",
    2: "RShoulder",
    3: "RElbow",
    4: "RWrist",
    5: "LShoulder",
    6: "LElbow",
    7: "LWrist",
    8: "RHip",
    9: "RKnee",
    10: "RAnkle",
    11: "LHip",
    12: "LKnee",
    13: "LAnkle",
    14: "REye",
    15: "LEye",
    16: "REar",
    17: "LEar"
}

# Grainulatity
JOINT_SECTIONS = ["JOINTS_MAPPING", "JOINTS_MAPPING_ARML", "JOINTS_MAPPING_ARMR"]
# Full
JOINTS_MAPPING = {
    1: [0, 1],
    2: [0, 14],
    3: [0, 15],
    4: [1, 2],
    5: [1, 5],
    6: [1, 8],
    7: [1, 11],
    8: [2, 3],
    9: [3, 4],
    10: [5, 6],
    11: [6, 7],
    12: [8, 9],
    13: [9, 10],
    14: [11, 12],
    15: [12, 13],
    16: [14, 16],
    17: [15, 17]
}

# Body Sections
# ArmL
JOINTS_ARML = [10, 11]
# ArmR
JOINTS_ARMR = [8, 9]
# LegL
JOINTS_LEGL = [14, 15]
# LegR
JOINTS_LEGR = [12, 13]
# Chest
JOINTS_CHEST = [6, 7]
# Head
JOINTS_HEAD = [2, 3, 16, 17]

def calculate_gradients_coarse(filename, label):
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

    for key in JOINTS_MAPPING:
        part_a = JOINTS_MAPPING[key][0]
        part_b = JOINTS_MAPPING[key][1]

        index_a = part_a * 3
        x1 = key_points[index_a]
        y1 = key_points[index_a + 1]
        c1 = key_points[index_a + 2]

        index_b = part_b * 3
        x2 = key_points[index_b]
        y2 = key_points[index_b + 1]
        c2 = key_points[index_b + 2]

        if x2 == x1 and x2 == 0:
            # point doesnt exist
            line += ",%0.4d,%0.3d,%0.3d" % (0, 0, 0)
        elif y2 == y1 and y2 == 0:
            # point doesnt exist
            line += ",%.4f,%.3f,%.3f" % (0, 0, 0)

        elif x2 == x1 and y2 == y1:
            # points are the same
            line += ",%.4f,%.3f,%.3f" % (0, 0, 0)

        elif x2 == x1:
            # gradient is infinite
            g = sys.maxsize
            line += ",%.4f,%.3f,%.3f" % (g, 0, 0)
        elif y2 == y1:
            # gradient is 0
            line += ",%.4f,%.3f,%.3f" % (0, c1, c2)
        else:
            g = (float(y2) - float(y1)) / (float(x2) - float(x1))
            line += ",%.4f,%.3f,%.3f" % (g, c1, c2)

    if not line == "":
        line = line[1:] + "," + str(correctness)

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
    file = open(os.path.join(input_dir, file_name), 'r')
    sets = []

    for line in file.readlines():
        if not line[:-2] in sets:
            sets.append(line[:-2])
    file.close()

    print("Sets to process: %d" % (len(sets)))

    json_dir = os.path.join(input_dir, "json")

    for data_set in sets:
        set_name_list = data_set.split("/")

        output_file_name = set_name_list[1] + "_" + set_name_list[2] + "_" + set_name_list[3] + "_" + set_name_list[4]
        output_file = open(output_dir + "/" + output_file_name + ".csv", "w+")

        for label in ["true", "false"]:
            set_dir = json_dir + "/" + label + "/" + data_set
            try:
                files = [f for f in os.listdir(set_dir) if os.path.isfile(os.path.join(set_dir, f))]

                lines = []
                for json_file in files:
                    # print(jsonFile)
                    lines.append(calculate_gradients_coarse(set_dir + "/" + json_file, label))

                for line in lines:
                    if not (line == "[]"):
                        # print(line)
                        output_file.write(line + "\n")
            except FileNotFoundError as e:
                print(e)
                continue

        output_file.close()
    print("Sets Processed")


def check_directory(path: str) -> None:
    """
    Checks if a directory exists, if not creates a new one
    :param path: The path of the directory
    """
    if not os.path.exists(path):
        os.makedirs(path)