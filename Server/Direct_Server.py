#!/usr/bin/env python

import os
import cgi
import cgitb
import uuid
import re
import time
import tensorflow as tf
import io
import base64
import cv2
import json
import sys
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from imageio import imread
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from DataCollection.utilities.fileutilities import check_directory

cgitb.enable(format="text")

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

TOKEN_EXPIRY = 16000
results = []
poses = []

model = load_model("./model.h5")
global graph
graph = tf.get_default_graph()
# graph = tf.get_default_graph()
# model.make_predict_function()


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        """
        Ends the response headers.
        """
        self.send_my_headers()
        BaseHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        """
        Adds Access-Control-Allow-Origin to the headers
        """
        self.send_header("Access-Control-Allow-Origin", "*")

    # GET
    def do_GET(self):

        current_time = time.time()
        global token_dict

        if None != re.search('/api/token', self.path):
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send message back to client
            key = str(uuid.uuid4())
            # value is the expiry of the token
            value = current_time + TOKEN_EXPIRY
            # add the uuid and the current time into the token dictionary
            add_token_to_dict(value, key)
            # Write content as utf-8 data
            self.wfile.write(bytes(key, "utf8"))
            return

        elif None != re.search('/api/*', self.path):
            token = self.path.split('/')[-1]

            # check expiry vs the dictionary
            value = {}
            try:
                value = token_dict[token]

            except Exception as e:
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "Invalid token"
                self.wfile.write(str.encode(message))
                return

            if value['expiry'] <= current_time:
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "Token has expired"
                self.wfile.write(str.encode(message))
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            status = 1.0
            try:
                # Send message back to client
                global video_dict
                expected_frames = (float(video_dict[token][1]) - float(video_dict[token][0])) * 30
                check_directory("server/data/output/" + token + "/json")
                processed_frames = os.listdir("../server/data/output/" + token + "/json")
                status = 1.0 * len(processed_frames) / expected_frames
                print(str(len(processed_frames)))
                print(str(expected_frames))
                print(str(status))

            except Exception as e:
                pass

            message = json.dumps({'token': token, 'status': status})
            # Write content as utf-8 data
            self.wfile.write(str.encode(message))
            return

    # POST
    def do_POST(self):
        """
        Accepts all post requests sent to the server, extracts the request data and video,
        then starts the computation pipeline.
        Then sends the response back to the client

        Note: this server is currently not able to handle more than 1 request at a time.
        :return:
        """
        global token_dict
        global video_dict

        print("post")

        current_time = time.time()

        # Check directorys all exist
        check_directory("server")
        check_directory("server/data/input")
        check_directory("server/data/output")

        fm = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

        data_values = json.loads(fm.getvalue('data'))
        token = data_values['token']
        img_number = data_values['counter']

        try:
            value = token_dict[token]

        except Exception as e:
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "Invalid token"
            print(message)
            self.wfile.write(str.encode(message))
            return

        if value['expiry'] <= current_time:
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "Token has expired"
            print(message)
            self.wfile.write(str.encode(message))
            return

        print(img_number)
        cv2_img = cv2.cvtColor(imread(io.BytesIO(base64.b64decode(fm.getvalue('file').split(',')[1]))),
                               cv2.COLOR_RGB2BGR)
        cv2_img = cv2.resize(cv2_img, (299, 299))
        cv2_img = (cv2_img[...,::-1].astype(np.float32)) / 255.0


        # do we want to save the image if so this is how we would
        # cv2.imwrite(token + "_" + str(img_number) + ".jpg", cv2_img)
        result = self.makePrediction(cv2_img)
        # results.append(result)

        # Return the response
        message = "Video was bad"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str.encode(result))

    def makePrediction(self, img):
        with graph.as_default():
            print(img.shape)
            x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
            x = x.reshape((1,) + x.shape)
            print(x.shape)
            result = model.predict(x)
            y_classes = result.argmax(axis=-1)
            print(y_classes)
            print(result)
            if result[0][0] > result[0][1]:
                return 0
            else:
                return 1


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


def run():
    """
    Runs the server for exercise analysis.
    Note that this server uses relative links so it must be run in the directory containing server.py
    :return:
    """

    print('Starting the exercise analysis server:')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
    print('Server is running.\n')
    httpd.serve_forever()


def add_token_to_dict(value, key):
    global token_dict
    print('\nAdding token to dict')
    print(token_dict)
    token_dict[key] = {'expiry': value, 'status': 0}


token_dict = {}
video_dict = {}
run()
