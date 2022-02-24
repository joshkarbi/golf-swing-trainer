'''
Use sample image/video frames to test data extraction, 
including detecting the coordinates of the golf ball and 
player position information.
'''

from cgi import test
import time
import pandas as pd
from metrics.metric_calculations import GolfSwingFeedbackInfoAndMetrics, analyze_datapoints, arm_pos_feedback 

import cv2
import pytest

from data_extraction.ball_detection import get_coordinates_of_golf_ball_in_image
from data_extraction.pose_detection import get_body_part_positions_in_image


def test_ball_detection_1():
    """Test using screenshot where ball is on the ground.
    """
    test_image = cv2.imread("assets/swing_frame_1.png")
    
    x, y = get_coordinates_of_golf_ball_in_image(
        test_image
    )
    
    # Check the detected coordinates are within 1.5% of expected.
    assert x == pytest.approx(170, rel=0.015)
    assert y == pytest.approx(438, rel=0.015)


def test_ball_detection_2():
    """Test using screenshot of ball in flight.
    """
    test_image = cv2.imread("assets/swing_frame_2.png")
    
    x, y = get_coordinates_of_golf_ball_in_image(
        test_image
    )
    
    # Check the detected coordinates are within 1.5% of expected.
    assert x == pytest.approx(342, rel=0.015)
    assert y == pytest.approx(328, rel=0.015)


def test_pose_detection_1():
    """Test using a screenshot.
    """
    test_image = cv2.imread("assets/swing_frame_1.png")

    pose_info = get_body_part_positions_in_image(
        image=test_image
    )

    # Confirm the labels are correct
    assert (
        pose_info["left_eye_y"] < 
        pose_info["left_shoulder_y"] < 
        pose_info["left_elbow_y"] < 
        pose_info["left_wrist_y"] < 
        pose_info["left_hip_y"] < 
        pose_info["left_knee_y"] <
        pose_info["left_ankle_y"]
    )

    assert (
        pose_info["right_eye_y"] < 
        pose_info["right_shoulder_y"] < 
        pose_info["right_elbow_y"] < 
        pose_info["right_wrist_y"] < 
        pose_info["right_hip_y"] <
        pose_info["right_knee_y"] < 
        pose_info["right_ankle_y"]
    )

    for body_part in ["eye", "ear", "shoulder", "wrist", "elbow", "hip", "ankle", "knee"]:
        assert pose_info[f"left_{body_part}_x"] > pose_info[f"right_{body_part}_x"]

    # Check some specific coordinates
    assert pose_info["left_eye_x"] > pose_info["right_eye_x"]
    assert pose_info["left_eye_x"] == pytest.approx(195, rel=0.02)
    assert pose_info["right_eye_x"] == pytest.approx(180, rel=0.02)

    assert pose_info["left_ankle_x"] > pose_info["right_ankle_x"]
    assert pose_info["left_ankle_x"] == pytest.approx(205, rel=0.02)
    assert pose_info["right_ankle_x"] == pytest.approx(155, rel=0.02)


def test_pose_detection_2():
    """Test using a screenshot.
    """
    test_image = cv2.imread("assets/swing_frame_2.png")

    pose_info = get_body_part_positions_in_image(
        image=test_image
    )

    # Confirm the labels are correct
    # Note: In this screenshow the wrists are below the hips
    assert (
        pose_info["left_eye_y"] < 
        pose_info["left_shoulder_y"] < 
        pose_info["left_elbow_y"] < 
        pose_info["left_hip_y"] < 
        pose_info["left_wrist_y"] < 
        pose_info["left_knee_y"] <
        pose_info["left_ankle_y"]
    )

    assert (
        pose_info["right_eye_y"] < 
        pose_info["right_shoulder_y"] < 
        pose_info["right_elbow_y"] < 
        pose_info["right_hip_y"] <
        pose_info["right_wrist_y"] < 
        pose_info["right_knee_y"] < 
        pose_info["right_ankle_y"]
    )

    for body_part in ["eye", "ear", "shoulder", "wrist", "elbow", "hip", "ankle", "knee"]:
        assert pose_info[f"left_{body_part}_x"] > pose_info[f"right_{body_part}_x"]

    # Check some specific coordinates
    assert pose_info["left_wrist_x"] > pose_info["right_wrist_x"]
    assert pose_info["left_wrist_x"] == pytest.approx(250, rel=0.02)
    assert pose_info["right_wrist_x"] == pytest.approx(225, rel=0.02)

    assert pose_info["left_elbow_x"] > pose_info["right_elbow_x"]
    assert pose_info["left_elbow_x"] == pytest.approx(240, rel=0.02)
    assert pose_info["right_elbow_x"] == pytest.approx(195, rel=0.02)


def test_pose_detection_performance():
    """Test the speed of pose detection.
    """
    test_image = cv2.imread("assets/swing_frame_1.png")

    start = time.time()
    _ = get_body_part_positions_in_image(
        image=test_image
    )
    end = time.time()
    
    # Max 33 ms allowed per frame.
    # A 10 second video uploaded by a user 
    # (shot at 30 fps) will take 10 seconds to analyze.
    assert end - start < 0.
    

def test_arm_pos_feedback_message():
    testObject = GolfSwingFeedbackInfoAndMetrics(10, 10, '', '')
    vid_analysis_df = pd.read_csv('C:/Users/chels/Documents/School/4th Year Semester 2/Capstone/golf-swing-trainer/backend/metrics/data_extraction.csv')
    analyze_datapoints(vid_analysis_df,testObject)
    assert testObject.arm_pos_feedback_msg == None
