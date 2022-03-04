"""
app.py

Main entrypoint into backend API.

Run on a local video file: python main.py --video assets/swing.gif
Run server: flask run --host=0.0.0.0 --port=5000
"""

import argparse
from threading import Thread
from typing import List, Dict, Optional, NamedTuple
from uuid import uuid4
from metrics.metric_calculations import (
    analyze_datapoints,
    GolfSwingFeedbackInfoAndMetrics,
)

from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from data_extraction.video_analysis import extract_data_out_of_video


class GolfSwingAnalysisResults(NamedTuple):
    """Results provided from this API to the client."""

    success: bool
    video_analyzed: str
    pieces_of_feedback: List[str]
    metrics: Dict[str, float]


class APIResults:
    analysis_results: Dict[
        str, Optional[GolfSwingAnalysisResults]
    ] = {}  # Map video_id's to results.


def analyze_video(
    video_file_path: Optional[str] = None, video_id: Optional[str] = None
) -> GolfSwingAnalysisResults:
    """Run the swing analysis on a video."""
    # Step 1: Extract data out of the video - pose and golf ball tracking data. Write and read to csv file.
    data = extract_data_out_of_video(video_file_name=video_file_path)

    # Step 2: Estimate key metrics using data and provide feedback on swing.
    swingObject = GolfSwingFeedbackInfoAndMetrics()
    analyze_datapoints(data, swingObject)

    results = GolfSwingAnalysisResults(
        success=True,
        video_analyzed=video_file_path.split("/")[-1],
        pieces_of_feedback=swingObject.feedback,
        metrics=swingObject.metrics,
    )

    if video_id:
        APIResults.analysis_results[video_id] = results

    return results


app = Flask(__name__)
CORS(app)


@app.route("/swing_to_analyze", methods=["POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["filename"]
        f.save(secure_filename(f.filename))

        video_id = str(uuid4())

        worker = Thread(target=analyze_video, args=(f.filename, video_id))
        worker.start()

        return {"success": True, "video_id": video_id}


@app.route("/results", methods=["GET"])
def send_client_results_if_available():
    video_id = request.args.get("video_id")
    if APIResults.analysis_results.get(video_id):
        return APIResults.analysis_results[video_id]._asdict()
    else:
        return {"success": False, "status": "processing"}


@app.route("/")
def hello():
    print("Running Flask server!!!")
    return '<form action="/swing_to_analyze" method="post" id="signup" enctype = "multipart/form-data"> <input type="file" id="myFile" name="filename">  <input type="submit"> </form>'


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="Path to the video of golf swing to analyze.")
    args = ap.parse_args()

    print("Running on local video file!!")
    results = analyze_video(video_file_path=args.video)
    print(f"Result of analysis: {results}")
