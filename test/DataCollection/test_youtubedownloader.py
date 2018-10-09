# coding=utf-8
from DataCollection.youtubedownloader.youtubedownloader import download_video, bulk_download_videos
import unittest
import os

class TestYouTubeDownloade(unittest.TestCase):

    def test_download_video(self):
        key = 'Omp0VC34oZc'
        if os.path.isfile(key):
            os.remove(key)

        path = os.getcwd()
        download_video(key, path)

        self.assertTrue(os.path.isfile(key), 'Video was not downloaded correctly')

        if os.path.isfile(key):
            os.remove(key)

    def test_bulk_download_video(self):
        keys = [{"identifier": "Omp0VC34oZc", "local": "false"}, {"identifier": "P78S_0ZOF6M", "local": "false"}]

        for key in keys:
            if os.path.isfile(key['identifier']):
                os.remove(key['identifier'])

        path = os.getcwd()
        bulk_download_videos(keys, path)

        for key in keys:
            self.assertTrue(os.path.isfile(key['identifier']), 'Video was not downloaded correctly by bulk downloader')
            if os.path.isfile(key['identifier']):
                os.remove(key['identifier'])

def main():
    unittest.main()

if __name__ == "__main__":
    main()
