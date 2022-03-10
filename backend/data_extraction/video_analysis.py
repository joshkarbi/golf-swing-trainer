from typing import NamedTuple, Generator, Any, Tuple

import cv2
import imageio
import pandas as pd
import numpy as np

from .ball_detection import get_coordinates_of_golf_ball_in_image
from .pose_detection import draw_prediction_on_image, get_body_part_positions_in_image, reset_crop_region, run_inference_and_overlay_movenet_on_frame

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


def get_video_frames(
    video_file_name: str,
) -> Generator[Tuple[Image, float], None, None]:
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
            timestamp += 1 / frames_per_second
        else:
            return


def extract_data_out_of_video(video_file_name: str) -> pd.DataFrame:
    """Extract data out of the video into
    a dataframe containing the observations.

    Parameters
    ----------
    video_file_name : str
        Path pointing to video to analyze.
    """

    observations = []
    prev_ball_x, prev_ball_y = None, None
    annotated_frames = []
    annotated_black_frames = []

    ball_keypoints = []
    annotated_frame = None
    annotated_black_frame = None
    
    for image, timestamp in get_video_frames(video_file_name=video_file_name):

        height, width = image.shape[0], image.shape[1]
        black_frame = np.zeros((height,width,3), np.uint8)

        ball_x, ball_y, keypoints = get_coordinates_of_golf_ball_in_image(image=image)
        if keypoints:
            ball_keypoints.append(keypoints)
        for keypoint in ball_keypoints:
            x, y = keypoint[0].pt
            center = (int(x), int(y))
            image = cv2.circle(img=image, center=center, radius=int(keypoint[0].size), color=(0,255,0), thickness=4)
            black_frame = cv2.circle(img=black_frame, center=center, radius=int(keypoint[0].size), color=(0,255,0), thickness=4)

        if not any([ball_x, ball_y]):
            ball_x = prev_ball_x
            ball_y = prev_ball_y

        annotated_frame, inference_res = run_inference_and_overlay_movenet_on_frame(image=image)
        black_frame = draw_prediction_on_image(black_frame, inference_res, None, True, 700)
        
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        annotated_black_frame = cv2.cvtColor(black_frame, cv2.COLOR_BGR2RGB)
        annotated_frames.append(annotated_frame)
        annotated_black_frames.append(annotated_black_frame)

        prev_ball_x = ball_x
        prev_ball_y = ball_y

        observations.append(
            GolfSwingVideoFrameInfo(
                timestamp=timestamp,
                video_width=width,
                video_height=height,
                ball_x=ball_x,
                ball_y=ball_y,
                **get_body_part_positions_in_image(image=image, keypoints_with_scores=inference_res)
            )
        )

    # Save debug data extraction
    res = pd.DataFrame(observations)
    res.to_csv("./static/debug_data_extraction.csv", na_rep="NULL")

    # Build the visualization
    for i, frame, black_frame in zip(range(len(annotated_frames)), annotated_frames, annotated_black_frames):
        annotated_frames[i] = frame[20:-40, 20:-20]
        annotated_black_frames[i] = black_frame[20:-40, 20:-20]
        
    output = np.stack(annotated_frames, axis=0)
    imageio.mimsave("./static/animation.gif", output, fps=20)
    imageio.mimsave("./static/animation.mp4", output, fps=20, format="MP4")
    output = np.stack(annotated_black_frames, axis=0)
    imageio.mimsave("./static/computer_vision.gif", output, fps=20)
    imageio.mimsave("./static/computer_vision.mp4", output, fps=20, format="MP4")
    imageio.imsave('./static/swing_overlay.png', annotated_frames[0])

    reset_crop_region()

    return res
