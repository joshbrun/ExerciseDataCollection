#!/usr/bin/env python

from shutil import copyfileobj
import os
import cgi
import cgitb;
import uuid

cgitb.enable(format="text")
from wsgiref.util import FileWrapper

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

import urllib
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from openpose.openPose import run_openpose_on_video
from utilities.fileutilities import check_directory
from jsonprocessing.processjson import process_json_for_server as process_json
from jsonprocessing.sequenceprocessjson import process_json_for_server as process_sequencial_json


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

    # POST
    def do_POST(self):
        """
        Accepts all post requests sent to the server, extracts the request data and video,
        then starts the computation pipeline.
        Then sends the response back to the client

        Note: this server is currently not able to handle more than 1 request at a time.
        :return:
        """
        # Check directorys all exist
        check_directory("server")
        check_directory("server/data/input")
        check_directory("server/data/output")

        id = str(uuid.uuid4())

        f = StringIO()
        fm = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        if "file" in fm:
            self.get_file_data(fm, id)
        else:
            print("ERROR")
            Exception("BAD")

        # Video at out.mp4
        data_values = json.loads(fm.getvalue('data'))

        exercise = (data_values['exercise'])
        view = (data_values['view'])
        gender = (data_values['gender'])
        start = (data_values['startTime'])
        end = (data_values['finishTime'])

        # Run the computation pipeline, (Similar to the training pipeline)
        self.process_pipeline(exercise, gender, view, id)

        # Return the response
        message = "Video was bad"
        self.send_response(200)
        self.send_header("content-type", "application/html")
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def process_pipeline(self, exercise, gender, view, id):
        """
        The process pipeline which takes the clients video,
        Breaks it into frames
        Runs openpose on all the frames
        Processes the json output of openpose
        Classify each json frame
        analysis the results
        return the results as a response to the client.
        """

        # Check the clients file exists

        check_directory("server")
        check_directory("server/data")
        check_directory("server/data/input")
        check_directory("server/data/output")

        # Run the server, when py server.py is called
        # run()
        if os.path.isfile("server/data/input/"+id+".mp4"):
            # Extract the frames
            # This is redundant currently, done directly by openpose

            output_dir = "server/data/output"
            # Run Open Pose on the frames
            run_openpose_on_video(id, "../server/data/input/", "../" + output_dir, True)

            # Create json Exercise file

            parts = ['all']
            with open('server/data/output/' + id + '/' + id + '.json', 'w') as outfile:
                data = ["/server/" + exercise + "/" + gender + "/" + view + "/" + "all"]
                json.dump(data, outfile)

            # Process the skeletal data
            process_json(os.path.join(output_dir, id), os.path.join(output_dir, id, "processedjson"), id)
            process_sequencial_json(os.path.join(output_dir, id), os.path.join(output_dir, id, "processedjson"), id)
            # Run Each frame against the model

            # Analysis the results

            # Form the response
            pass

    def get_file_data(self, form, id):
        """
        Gets the file data from the request.
        this request form contains the name, gender, exercise and view of the request.
        :param form: The data set within the request.
        :return: The path to the request input video.
        """
        fn = form.getvalue((os.getcwd()), "server/data/input/"+id+".mp4")
        open(fn, 'w').close()

        with open(fn, 'wb') as out:
            out.write(form['file'].file.read())
        return "server/data/input/"+id+".mp4"



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
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('Server is running.\n')
    httpd.serve_forever()

run()

