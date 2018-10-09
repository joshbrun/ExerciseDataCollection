# coding=utf-8
from DataCollection.videosplitter.videosplitter import split_videos, get_seconds
import unittest
import os

class TestVideoSplitter(unittest.TestCase):

    def test_get_seconds(self):
        result = get_seconds("1:1:1")
        self.assertEqual(3661, result)

    def test_get_seconds_zero(self):
        result = get_seconds("0:0:0")
        self.assertEqual(0, result)

    def test_get_seconds_to_many_seconds(self):
        result = get_seconds("0:0:61")
        self.assertEqual(61, result)

    def test_get_seconds_to_many_hours(self):
        result = get_seconds("0:25:0")
        self.assertEqual(1500, result)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
