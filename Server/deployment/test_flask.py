from flask import Flask, redirect, url_for, request, send_from_directory, session
import os
from flask_cors import CORS, cross_origin
import uuid


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
from os import makedirs
from os.path import exists

from imageio import imread
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

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

app = Flask(__name__, static_folder='p4p-client-app/build')
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/api/token", methods=['GET'])
def get_token():
    session['username'] = 0
    current_time = time.time()
    global token_dict

    # Send message back to client
    key = str(uuid.uuid4())
    # value is the expiry of the token
    value = current_time + TOKEN_EXPIRY
    # add the uuid and the current time into the token dictionary
    add_token_to_dict(value, key)
    return key

@app.route("/", methods=['POST'])
def do_post():
    """
    Accepts all post requests sent to the server, extracts the request data and video,
    then starts the computation pipeline.
    Then sends the response back to the client

    Note: this server is currently not able to handle more than 1 request at a time.
    :return:
    """
    global token_dict
    global video_dict
    print(session['username'])
    session['username'] = session['username'] + 1
    print("post")

    current_time = time.time()

    # Check directorys all exist
    check_directory("server")
    check_directory("server/data/input")
    check_directory("server/data/output")

    cv2_img = cv2.cvtColor(imread(io.BytesIO(base64.b64decode(request.form['file'].split(',')[1]))),
                            cv2.COLOR_RGB2BGR)
    cv2_img = cv2.resize(cv2_img, (299, 299))
    cv2_img = (cv2_img[...,::-1].astype(np.float32)) / 255.0

    result = makePrediction(cv2_img)
    return str(result)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("p4p-client-app/build/" + path):
        return send_from_directory('p4p-client-app/build', path)
    else:
        return send_from_directory('p4p-client-app/build', 'index.html')


def makePrediction(img):
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

def add_token_to_dict(value, key):
    global token_dict
    print('\nAdding token to dict')
    print(token_dict)
    token_dict[key] = {'expiry': value, 'status': 0}

def check_directory(path: str) -> None:
    """
    Helper function to make sure that a directory exists at a path, if not create one.
    :param path:
    """
    if not exists(path):
        makedirs(path)


token_dict = {}
video_dict = {}

if __name__ == '__main__':
    app.run(ssl_context="adhoc", port=5000, threaded=True)
