'''
app.py

Main entrypoint into backend API.

Run on a local video file: python main.py --video assets/swing.gif
Run server: export FLASK_ENV=<development/prod> && flask run
'''

import argparse
from typing import Optional

from flask import Flask, request
from werkzeug.utils import secure_filename

from data_extraction.video_analysis import analyze_video

def main(video_file_path: Optional[str] = None):
    """Run the swing analysis on a video.

    TODO: Start a server to accept incoming videos to analyze.
    """

    # Step 1: Extract data out of the video - pose and golf ball tracking data.
    data = analyze_video(video_file_name = video_file_path)

    # Step 2: Estimate key metrics using data.

    # Step 3: Use metrics to provide score/feedback on swing.

    pass

app = Flask(__name__)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      print(request.files)
      f = request.files['filename']
      f.save(secure_filename(f.filename))
      return 'File uploaded successfully. Analysis starting...'

@app.route("/")
def hello():
    print("Running Flask server!!!")
    return "<form action=\"/uploader\" method=\"post\" id=\"signup\" enctype = \"multipart/form-data\"> <input type=\"file\" id=\"myFile\" name=\"filename\">  <input type=\"submit\"> </form>"

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="Path to the video of golf swing to analyze.")
    args = ap.parse_args()

    print("Running on local video file!!")
    main(video_file_path = args.video)