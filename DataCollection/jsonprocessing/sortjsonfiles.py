# coding=utf-8

"""
sorts the json files from a single directory into a multiple directories.
"""

from os import listdir, getcwd, rename, remove
from os.path import isfile, join
import sys

sys.path.append(join(getcwd(), "utilities"))
from DataCollection.utilities.fileutilities import check_directory


def sort_json_files(input_dir):
    """
    sorts json files
    """
    # Take a file in the form:
    # true_squat_male_left_up_t2b8fDsAlFs_00035_keypoints
    # into
    # /true/squat/male/left/up/t2b8fDsAlFs_00035_keypoints
    json_files = []
    json_dir = input_dir + "/" #getcwd() + "/data/json/"

    files = [f for f in listdir(json_dir) if isfile(join(json_dir, f))]
    file_count = len(files)
    excluded_count = 0
    included_count = len(files)
    print("\nSorting %d files" % file_count)
    for file_name in files:
        dir_names = file_name.split("_")
        new_dir = dir_names[0] + "/" + dir_names[1] + "/" + dir_names[2] + "/" + dir_names[3] + "/" + dir_names[4] + "/"
        new_file = dir_names[5] + "_" + dir_names[6] + "_" + dir_names[7]
        check_directory(json_dir + new_dir)

        try:
            rename(json_dir + file_name, json_dir + new_dir + new_file)
            if not (new_dir in json_files):
                json_files.append(
                    "/" + dir_names[1] + "/" + dir_names[2] + "/" + dir_names[3] + "/" + dir_names[4] + "/")
        except FileExistsError:
            excluded_count += 1
            included_count -= 1
            remove(json_dir + file_name)

    f = open("data/exerciseList", 'a+')
    json_files = set(json_files)
    for file_name in json_files:
        print(file_name)
        f.write(file_name + "\n")

    print("Json created for %d/%d files, %d already existed " % (included_count, file_count, excluded_count))
    f.close()
