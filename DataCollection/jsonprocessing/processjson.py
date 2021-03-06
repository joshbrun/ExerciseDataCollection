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
from DataCollection.utilities.fileutilities import check_directory

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

# Reflection mapping
REFLECTION_POINTS = [
    (17, 18),
    (15, 16),
    (2, 5),
    (3, 6),
    (4, 7),
    (9, 12),
    (10, 13),
    (11, 14),
    (22, 19),
    (23, 20),
    (24, 21)
]

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
    elif label == "server":
        correctness = '?'

    line = ""
    file = open(filename, 'r')
    lines = file.readline()
    people = json.loads(lines)['people']

    if len(people) > 0:
        # If there are more than one person in the frame only use the first.
        key_points = people[0]['pose_keypoints_2d']

        right_hip_x = key_points[8 * 3]
        right_hip_y = key_points[8 * 3 + 1]

        # normalise around the right hip
        for i in range(0, len(key_points)):
            if i % 3 == 0:
                key_points[i] -= right_hip_x
            if i % 3 == 1:
                key_points[i] -= right_hip_y
        line = ",".join(map(str, key_points))
        line += "," + str(correctness)

        file.close()

    return line

def calculate_std(filename, label):
    """
    :param filename:
    :param label:
    :return:
    """
    # print("Calculating Gradients for filename: "+filename+", label: "+label);
    correctness = 0
    if label == "true":
        correctness = 1
    elif label == "server":
        correctness = '?'

    line = ""
    file = open(filename, 'r')
    lines = file.readline()
    people = json.loads(lines)['people']

    if len(people) > 0:
        # If there are more than one person in the frame only use the first.
        key_points = people[0]['pose_keypoints_2d']

        line = ",".join(map(str, key_points))
        line += "," + str(correctness)

        file.close()

    return line

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
    elif label == "server":
        correctness = '?'

    line = ""
    file = open(filename, 'r')
    lines = file.readline()
    people = json.loads(lines)['people']

    if len(people) > 0:
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

def process_json(input_dir, output_dir):
    """
    Processes the Json files into trainable data sets.
    :param input_dir: The location of the Json data.
    :param output_dir: The location of the Training directory.
    """
    expanding_set = True
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

        output_file_name = set_name_list[1] + "_" + set_name_list[2] + "_" + set_name_list[3] + "_" + set_name_list[4]
        agg_output_file_name = set_name_list[1] + "_" + set_name_list[3]
        output_agg_file = open(output_dir + "/" + agg_output_file_name + ".csv", "a")
        gradient_output_agg_file = open(output_dir + "/gradient_" + agg_output_file_name + ".csv", "a")
        hcs_output_agg_file = open(output_dir + "/" + "hcs_" + agg_output_file_name + ".csv", "a")
        mirrored_output_agg_file = open(output_dir + "/mirrored_" + agg_output_file_name + ".csv", "a")
        mirrored_hcs_output_agg_file = open(output_dir + "/" + "mirrored_hcs_" + agg_output_file_name + ".csv", "a")
        scaled_output_agg_file = open(output_dir + "/" + "scaled_" + agg_output_file_name + ".csv", "a")
        scaled_hcs_output_agg_file = open(output_dir + "/" + "scaled_hcs_" + agg_output_file_name + ".csv", "a")

        for label in ['true', 'false']:
            set_dir = json_dir + "/" + label + "/" + data_set
            try:
                files = [f for f in listdir(set_dir) if isfile(join(set_dir, f))]
                files.sort()
                lines = []
                std_lines = []
                hcs_lines = []
                for json_file in files:
                    lines.append(calculate_gradients_coarse(set_dir + "/" + json_file, label))
                    hcs_lines.append(calculate_hcs(set_dir + "/" + json_file, label))
                    std_lines.append(calculate_std(set_dir + "/" + json_file, label))
                
                for line in lines:
                    if not line == "":
                        gradient_output_agg_file.write(line + "\n")

                for line in std_lines:
                    if not line == "":
                        scaled = normalise([float(x) for x in line.split(',')], 0, 75)
                        scaled = normalise(scaled, 1, 75)
                        scaled[-1] = int(scaled[-1])
                        scaled_output_agg_file.write(",".join(map(str, scaled)) + "\n")
                        output_agg_file.write(line + "\n")
                        for ex_line in expand_set(line):
                            if not (ex_line == ""):
                                mirrored_output_agg_file.write(ex_line + "\n")

                for line in hcs_lines:
                    if not line == "":
                        scaled = normalise([float(x) for x in line.split(',')], 0, 75)
                        scaled = normalise(scaled, 1, 75)
                        scaled[-1] = int(scaled[-1])
                        scaled_hcs_output_agg_file.write(",".join(map(str, scaled)) + "\n")
                        hcs_output_agg_file.write(line + "\n")
                        for ex_line in expand_set(line):
                            if not (ex_line == ""):
                                mirrored_hcs_output_agg_file.write(ex_line + "\n")

            except FileNotFoundError as e:
                print(e)
                continue

        output_agg_file.close()
        gradient_output_agg_file.close()
        hcs_output_agg_file.close()
        mirrored_output_agg_file.close()
        mirrored_hcs_output_agg_file.close()
    print("Sets Processed")

def process_json_for_server(input_dir, output_dir, id):
    """
        Processes the Json files into trainable data sets.
        :param input_dir: The location of the Json data.
        :param output_dir: The location of the Training directory.
        """
    expanding_set = False
    print("\nConverting the separate Json files into a Trainable Vector Set")
    check_directory(output_dir)
    check_directory(input_dir)

    # Read the sets
    file = open(join(input_dir, id+".json"), 'r')
    sets = []

    for line in file.readlines():
        if not line[:-2] in sets:
            sets.append(line[:-2])
    file.close()

    print("Sets to process: %d" % (len(sets)))

    json_dir = input_dir  # join(input_dir, "json")

    for data_set in sets:
        set_name_list = data_set.split("/")
        output_file_name = set_name_list[1] + "_" + set_name_list[2] + "_" + set_name_list[3] + "_" + set_name_list[4]
        # output_file = open(output_dir + "/" + output_file_name + ".csv", "w+")
        # hcs_output_file = open(output_dir + "/" + "hcs_" + output_file_name + ".csv", "w+")
        agg_output_file_name = set_name_list[1] + "_" + set_name_list[3]
        output_agg_file = open(output_dir + "/" + agg_output_file_name + ".csv", "a")
        hcs_output_agg_file = open(output_dir + "/" + "hcs_" + agg_output_file_name + ".csv", "a")
        mirrored_output_agg_file = open(output_dir + "/mirrored_" + agg_output_file_name + ".csv", "a")
        mirrored_hcs_output_agg_file = open(output_dir + "/" + "mirrored_hcs_" + agg_output_file_name + ".csv", "a")

        for label in ['server']:
            set_dir = json_dir +'/json'

            files = [f for f in listdir(set_dir) if isfile(join(set_dir, f))]
            files.sort()
            lines = []
            hcs_lines = []
            for json_file in files:
                lines.append(calculate_gradients_coarse(set_dir + "/" + json_file, label))
                hcs_lines.append(calculate_hcs(set_dir + "/" + json_file, label))

            for line in lines:
                if not line == "":
                    output_agg_file.write(line + "\n")
                    for ex_line in expand_set(line):
                        if not (ex_line == ""):
                            # output_file.write(line + "\n")
                            mirrored_output_agg_file.write(ex_line + "\n")

            for line in hcs_lines:
                if not line == "":
                    hcs_output_agg_file.write(line + "\n")
                    for ex_line in expand_set(line):
                        if not (ex_line == ""):
                            # hcs_output_file.write(ex_line + "\n")
                            mirrored_hcs_output_agg_file.write(ex_line + "\n")



        output_file.close()
    print("Sets Processed")

def expand_set(line):
    # return [line]
    line = line.split(",")
    lines = []
    lines.append(line)
    lines.append(mirror(line))
    # new_lines = []
    # for l in lines:
    #     new_lines.append(scale(l, 0.8))
    #     new_lines.append(scale(l, 1.2))
    # lines += new_lines
    final_lines = []
    for l in lines:
        final_lines.append(",".join(map(str, l)))
    return final_lines

def mirror(line):
    reversed_points = scale(line, -1)
    for swap_points in REFLECTION_POINTS:
        reversed_points[swap_points[0] * 3], reversed_points[swap_points[1] * 3] = reversed_points[swap_points[1] * 3], reversed_points[swap_points[0] * 3]
    return scale(line, -1)

def scale(line, scale_factor):
    line_copy = line.copy()
    line_copy = [line[i] if i % 3 == 2 or i + 1 == len(line) else scale_factor * float(line[i]) for i in range(len(line))]
    return line_copy

def normalise(data, index, length, skip=3):
    max_x = -10
    min_x = 10
    min_ind = -1
    for y in range(index, length, skip):
        val = data[y]
        if val > max_x:
            max_x = val
        elif val < min_x:
            min_x = val
            min_ind = y

    factor = 2 / (max_x + abs(min_x))
    shift = -1 - data[min_ind] * factor

    for y in range(index, length, skip):
        data[y] = data[y] * factor + shift
    
    return data
