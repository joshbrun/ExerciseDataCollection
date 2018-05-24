# coding=utf-8

"""
Handles the running of OpenPose on a directory of images.
"""

import os
import sys


def check_openpose_directories():
    """

    :return:
    """
    if not os.path.isdir("./openpose/bin"):
        print("./openpose/bin Not found.")
        return False
    elif not os.path.isdir("./openpose/include"):
        print("./openpose/include Not found.")
        return False
    elif not os.path.isdir("./openpose/lib"):
        print("./openpose/lib Not found.")
        return False
    elif not os.path.isdir("./openpose/models"):
        print("./openpose/models Not found.")
        return False
    else:
        print("All openpose directories have been found.")
        return True


def run_openpose(input_dir, output_dir):
    """

    :param input_dir:
    :param output_dir:
    """
    if check_openpose_directories():
        print(input_dir)
        print(output_dir)

        # This requires the
        # Runs openpose on all the images in the images in the input dir,
        # and outputs all the Json files in the output dir
        print(os.getcwd())

        output_dir = os.path.join("..", output_dir)
        input_dir = os.path.join("..", input_dir)

        openpose = ".\\bin\\OpenPoseDemo.exe"
        command = openpose + " --image_dir " + input_dir + " --write_json " + output_dir + " --display 0" \
                                                                                                       " -render_pose 0"
        # Run the command

        print("Running openpose")
        print("Frames in: " + input_dir)
        print("Outputting Json in: " + output_dir)



        print(os.getcwd())
        print(command)
        os.chdir(os.path.join(os.getcwd(), "openpose"))
        print(os.getcwd())

        os.system(command)
        os.chdir(os.getcwd()[:-9])
        print(os.getcwd())
    else:
        print("ERROR: openpose is not in the required location.")
        sys.exit()
