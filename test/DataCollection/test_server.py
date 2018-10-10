# coding=utf-8
from DataCollection.server import add_token_to_dict
import unittest
import os
import uuid

class TestVideoSplitter(unittest.TestCase):

    def test_add_token(self):
        token_dict = add_token_to_dict("1",1)
        self.assertEqual(token_dict[1]['expiry'], "1")

    def test_add_token_uuid(self):
        id = uuid.uuid4()
        token_dict = add_token_to_dict(4321, id)
        self.assertEqual(token_dict[id]['expiry'], 4321)

def main():
    unittest.main()


if __name__ == "__main__":
    main()
