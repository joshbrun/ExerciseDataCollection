# coding=utf-8

"""
Handles the running of OpenPose on a directory of images.
"""

import os
import sys
from utilities.fileutilities import check_directory


def check_openpose_directories():
    """

    :return:
    """

    if os.name == "posix":
        # Todo: change this to actually check shit on linux
        return True
    else:
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


def run_openpose(input_dir, output_dir, keypoint_scale):
    """

    :param input_dir:
    :param output_dir:
    """
    if check_openpose_directories():
        # This requires the
        # Runs openpose on all the images in the images in the input dir,
        # and outputs all the Json files in the output dir

        output_dir = os.path.join("..", output_dir)
        input_dir = os.path.join("..", input_dir)

        if os.name == "posix":
            openpose = "./build/examples/openpose/openpose.bin"
        else:
            openpose = ".\\bin\\OpenPoseDemo.exe"
        
        # keypoint_scale 4 normalises between 1 and -1
        command = openpose + " --image_dir " + input_dir + " --write_json " + output_dir + " --display 0 -render_pose 0 --keypoint_scale " + str(keypoint_scale)
        # Run the command

        print("Running OpenPose")
        print("Frames in: " + input_dir)
        print("Outputting Json in: " + output_dir)

        os.chdir(os.path.join(os.getcwd(), "openpose"))
        os.system(command)
        os.chdir(os.getcwd()[:-9])
    else:
        print("ERROR: openpose is not in the required location.")
        sys.exit()

def run_openpose_on_video(video_path, output_dir, create_skeletial_overlayed_video):
    """
    Runs openpose directly against a video, extracting the json frames, but also creates an optional video with the 
    skeletal mapping overlapped.
    :param video_path: The path to the video, Should be full path, so join(os.path.getcwd(), path)
    :param output_dir: The directory to store the json output, (Will be stored in subdir /json)
    :param create_skeletial_overlayed_video: Boolean to determine if a video is requested, (Will be stored in /video)
    """
    if check_openpose_directories():
        # This requires the
        # Runs openpose on all the images in the images in the input dir,
        # and outputs all the Json files in the output dir

        # Check the output_dir exist
        check_directory(output_dir)

        # Check the output subdirs exist
        check_directory(os.path.join(output_dir, 'json'))
        if(create_skeletial_overlayed_video):
            check_directory(os.path.join(output_dir, 'video'))

        if os.name == "posix":
            openpose = "./build/examples/openpose/openpose.bin"
        else:
            openpose = ".\\bin\\OpenPoseDemo.exe"

        os.path.join("..", video_path)
        os.path.join("..", output_dir)

        # keypoint_scale 4 normalises between 1 and -1
        command = openpose + " --video " + video_path + " --write_json " + output_dir + " --write_video "+os.path.join(output_dir,'video','out.avi')+" --display 0 "

        # Run the command

        print("Running OpenPose")
        print("Video:", video_path)
        print("Output:", output_dir)

        # cd into the openpose directory
        os.chdir(os.path.join(os.getcwd(), "openpose"))

        # Run Openpose relative to the openpose directory
        os.system(command)
        # Revert back to the main dir
        os.chdir(os.getcwd()[:-9])
    else:
        print("ERROR: openpose is not in the required location.")
        sys.exit()