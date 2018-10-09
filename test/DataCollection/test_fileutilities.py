# coding=utf-8
from DataCollection.utilities.fileutilities import check_directory
import unittest
import os

class TestFileUtilities(unittest.TestCase):

    def test_check_directory_with_no_existing(self):
        name = 'temp-folder-testing-only'

        if os.path.isdir(name):
            os.removedirs(name)

        check_directory(name)

        self.assertTrue(os.path.isdir(name), 'Folder wasn\'t created when it should have been.')

        if os.path.isdir(name):
            os.removedirs(name)

    def test_check_directory_on_an_existing_directory(self):
        name = 'temp-folder-testing-only'

        if not os.path.isdir(name):
            os.makedirs(os.path.join(os.getcwd(), name))

        check_directory(name)

        self.assertTrue(os.path.isdir(name), 'Folder was deleted when it shouldn\'t have been.')

        if os.path.isdir(name):
            os.removedirs(name)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
