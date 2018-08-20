# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform

dir_path = os.path.dirname(os.path.realpath(__file__))
if platform == "win32": sys.path.append(dir_path + '/../../python/openpose/')
else: sys.path.append('../../python')

# Parameters for OpenPose. Take a look at C++ OpenPose example for meaning of components. Ensure all below are filled
try:
    from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

class OpenPoseWrapper(object):

    def __init__(self, params=None):
        
        params = dict()
        params["logging_level"] = 3
        params["output_resolution"] = "-1x-1"
        params["net_resolution"] = "-1x368"
        params["model_pose"] = "BODY_25"
        params["alpha_pose"] = 0.6
        params["scale_gap"] = 0.3
        params["scale_number"] = 1
        params["render_threshold"] = 0.05
        # If GPU version is built, and multiple GPUs are available, set the ID here
        params["num_gpu_start"] = 0
        params["disable_blending"] = False
        # Ensure you point to the correct path where models are located
        params["default_model_folder"] = dir_path + "/../../../models/"
        # Construct OpenPose object allocates GPU memory
        self.openpose = OpenPose(params)

    def runOpenPoseOnImage(self, img):
        keypoints, output_image = self.openpose.forward(img, True)
        # cv2.imwrite("trial.jpg", output_image)
        return keypoints

op = OpenPoseWrapper()
op.runOpenPoseOnImage("asdf")