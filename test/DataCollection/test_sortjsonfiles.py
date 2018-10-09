# coding=utf-8
from DataCollection.jsonprocessing.sortjsonfiles import sort_json_files
import unittest
import os
import shutil

class TestSortJsonFiles(unittest.TestCase):

    def test_sort_json_same_dir(self):
        file_1 = 'true_squat_male_left_up_t2b8fDsAlFs_00035_keypoints'
        file_2 = 'true_squat_male_left_up_t2b8fDsAlFs_00036_keypoints'

        expected_1 = os.path.join('true', 'squat', 'male', 'left', 'up', 't2b8fDsAlFs_00035_keypoints.json')
        expected_2 = os.path.join('true', 'squat', 'male', 'left', 'up', 't2b8fDsAlFs_00036_keypoints.json')

        os.mkdir("temp")
        os.mkdir("data")

        with open(os.path.join('data', 'exerciseList'), "w+"):
            pass
        with open(os.path.join('temp', file_1+".json"), "w+"):
            pass
        with open(os.path.join('temp', file_2+".json"), "w+"):
            pass

        sort_json_files('temp')

        expected_path_1 = os.path.join(os.getcwd(), 'temp', expected_1 )
        expected_path_2 = os.path.join(os.getcwd(), 'temp', expected_2 )

        self.assertTrue(os.path.isfile(expected_path_1))
        self.assertTrue(os.path.isfile(expected_path_2))

        if os.path.isfile(expected_path_1):
            os.remove(expected_path_1)

        if os.path.isfile(expected_path_2):
            os.remove(expected_path_2)

        if os.path.isdir('temp'):
            shutil.rmtree(os.path.join(os.getcwd(), 'temp'))

    def test_sort_json_different_dir(self):
        file_1 = 'true_squat_male_left_up_t2b8fDsAlFs_00035_keypoints'
        file_2 = 'false_standing_female_right_down_t2b8fDsAlFs_00036_keypoints'

        expected_1 = os.path.join('true', 'squat', 'male', 'left', 'up', 't2b8fDsAlFs_00035_keypoints.json')
        expected_2 = os.path.join('false', 'standing', 'female', 'right', 'down', 't2b8fDsAlFs_00036_keypoints.json')

        if os.path.isdir('temp'):
            shutil.rmtree(os.path.join(os.getcwd(), 'temp'), ignore_errors=True)
        if os.path.isdir('data'):
            shutil.rmtree(os.path.join(os.getcwd(), 'data'), ignore_errors=True)

        os.mkdir("temp")
        os.mkdir("data")

        with open(os.path.join('data', 'exerciseList'), "w+"):
            pass
        with open(os.path.join('temp', file_1+".json"), "w+"):
            pass
        with open(os.path.join('temp', file_2+".json"), "w+"):
            pass

        sort_json_files('temp')

        expected_path_1 = os.path.join(os.getcwd(), 'temp', expected_1 )
        expected_path_2 = os.path.join(os.getcwd(), 'temp', expected_2 )

        self.assertTrue(os.path.isfile(expected_path_1))
        self.assertTrue(os.path.isfile(expected_path_2))

        if os.path.isfile(expected_path_1):
            os.remove(expected_path_1)

        if os.path.isfile(expected_path_2):
            os.remove(expected_path_2)

        if os.path.isfile(os.path.join(os.getcwd(), 'data', 'exerciseList')):
            os.remove(os.path.join(os.getcwd(), 'data', 'exerciseList'))

        if os.path.isdir('temp'):
            shutil.rmtree(os.path.join(os.getcwd(), 'temp'), ignore_errors=True)
        if os.path.isdir('data'):
            shutil.rmtree(os.path.join(os.getcwd(), 'data'), ignore_errors=True)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
