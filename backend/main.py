'''
main.py

Main entrypoint into backend API.

Run on a local video file: python main.py --video assets/swing.gif
'''

import argparse
from typing import Optional

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

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="Path to the video of golf swing to analyze.")
    args = ap.parse_args()

    main(video_file_path = args.video)