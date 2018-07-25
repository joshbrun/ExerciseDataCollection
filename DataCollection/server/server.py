#!/usr/bin/env python

from shutil import copyfileobj
import os
import cgi
import cgitb; cgitb.enable(format="text")
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
      check_directory("data")
      check_directory("data/input")
      check_directory("data/output")

      f = StringIO()
      fm = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
      if "file" in fm:
          self.get_file_data(fm)
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

      video_path = os.path.join(os.getcwd(),"data/clientVideos.json")

      # Currently only one user is expected at once, so just create a new dictionary
      videos_dict = { "Videos":[]}

      videos_dict['Videos'].append({
          "identifier": "out",
          "exercise": exercise,
          "sex": gender,
          "local": 'true',
          "parts": [{
              "name": "full",
              "label":"client",
              "view":view,
              "startTime":start,
              "endTime":end
          }]
      })

      with open(video_path, "w") as client_videos:
          client_videos.write(json.dumps(videos_dict))

      # Run the computation pipeline, (Similar to the training pipeline)
      # self.process_pipeline()


      # Return the response
      message = "Video was bad"
      self.send_response(200)
      self.send_header("content-type", "application/html")
      self.end_headers()
      self.wfile.write(bytes(message, "utf8"))


  def get_file_data(self, form):
      """
      Gets the file data from the request.
      this request form contains the name, gender, exercise and view of the request.
      :param form: The data set within the request.
      :return: The path to the request input video.
      """
      for value in form:
          print(value)
      fn = form.getvalue((os.getcwd()),"data/input/out.mp4")
      print(fn)
      open(fn, 'w').close()

      with open(fn, 'wb') as out:
        out.write(form['file'].file.read())
      return "data/input/out.mp4"

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

# Run the server, when py server.py is called
run()
