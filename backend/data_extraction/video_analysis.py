
from typing import NamedTuple, Generator, Any, Tuple

import cv2
import pandas as pd

from .ball_detection import get_coordinates_of_golf_ball_in_image
from .pose_detection import get_body_part_positions_in_image

class GolfSwingVideoFrameInfo(NamedTuple):
    """Info from 1 frame in a golf swing video.
    All coordinates / dimensions are in pixels.
    """
    timestamp: float

    video_width: int
    video_height: int

    ball_x: int
    ball_y: int

    nose_x: float
    nose_y: float 
    left_eye_x: float
    left_eye_y: float
    right_eye_x: float
    right_eye_y: float
    left_ear_x: float
    left_ear_y: float
    right_ear_x: float
    right_ear_y: float
    left_shoulder_x: float
    left_shoulder_y: float
    right_shoulder_x: float
    right_shoulder_y: float
    left_elbow_x: float
    left_elbow_y: float
    right_elbow_x: float
    right_elbow_y: float
    left_wrist_x: float
    left_wrist_y: float
    right_wrist_x: float
    right_wrist_y: float
    left_hip_x: float
    left_hip_y: float
    right_hip_x: float
    right_hip_y: float
    left_knee_x: float
    left_knee_y: float
    right_knee_x: float
    right_knee_y: float
    left_ankle_x: float
    left_ankle_y: float
    right_ankle_x: float
    right_ankle_y: float

Image = Any
def get_video_frames(video_file_name: str) -> Generator[Tuple[Image, float], None, None]:
    """Generator to pull image frames and 
    timestamps out of a video file.

    Parameters
    ----------
    video_file_name : str
        Name of file.
    """

    vs = cv2.VideoCapture(video_file_name)
    frames_per_second = vs.get(cv2.CAP_PROP_FPS)
    timestamp = 0

    while True:
        is_next_frame, frame = vs.read()
        if is_next_frame:
            yield [frame, round(timestamp, 2)]
            timestamp += 1/frames_per_second 
        else:
            return
            
def analyze_video(video_file_name: str) -> pd.DataFrame:
    """Extract data out of the video into 
    a dataframe containing the observations.

    Parameters
    ----------
    video_file_name : str
        Path pointing to video to analyze.
    """

    observations = []
    prev_ball_x, prev_ball_y = None, None

    for image, timestamp in get_video_frames(video_file_name=video_file_name):

        height, width = image.shape[0], image.shape[1]

        ball_x, ball_y = get_coordinates_of_golf_ball_in_image(image = image)
        if not any([ball_x, ball_y]):
            ball_x = prev_ball_x
            ball_y = prev_ball_y
        prev_ball_x = ball_x
        prev_ball_y = ball_y

        observations.append(
            GolfSwingVideoFrameInfo(
                timestamp=timestamp,
                video_width=width,
                video_height=height,
                ball_x=ball_x,
                ball_y=ball_y,
                **get_body_part_positions_in_image(image = image)
            )
        )

    res = pd.DataFrame(observations)
    res.to_csv("debug_data_extraction.csv", na_rep='NULL')
    return res