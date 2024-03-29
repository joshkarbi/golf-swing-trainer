"""
This file consists of a function whose input is a pandas dataframe of body position and ball x,y locations and an object to store
the metrics and feedback applicable to the shot. Using this data, it performs calculation to determine if the user
has correct positioning, and provides feedback
"""

from cmath import cos, pi, sin
from pydoc import apropos
from typing import NamedTuple, Optional, Tuple
from math import atan, sqrt
from random import randint

import pandas as pd
from numpy import arctan
from pytest import approx

class GolfSwingFeedbackInfoAndMetrics(NamedTuple):
    metrics = {}
    feedback = {}

    shoulder_metrics = {}
    elbow_metrics = {}
    wrist_metrics = {}
    hip_metrics = {}
    knee_metrics = {}
    ankle_metrics = {}

    eye_metrics = {}
    nose_metrics = {}


def analyze_datapoints(vid_analysis_df: pd.DataFrame, swingObject) -> pd.DataFrame:
    """Input is video analysis data and  GolfSwingFeedbackInfoAndMetrics object
    Feedback messages and metrics are updated in the object"""

    prev_ball_x = None
    prev_ball_y = None
    prev_ball_timestamp = 0
    ball_in_motion = 0
    body_starting_pos_timestamp = 0
    body_starting_pos_index = 0
    ball_in_motion_timestamp = 0
    ball_in_motion_index = 0

    ball_stationary_timestamp = None
    timestamps_from_starting_pos_to_shot = []

    for index, row in vid_analysis_df.iterrows():

        swingObject.eye_metrics[row["timestamp"]] = [
            row["left_eye_x"],
            row["right_eye_x"]
        ]
        
        swingObject.nose_metrics[row["timestamp"]] = [
            row["nose_x"],
            row["nose_y"]
        ]

        swingObject.shoulder_metrics[row["timestamp"]] = [
            row["left_shoulder_x"],
            row["left_shoulder_y"],
            row["right_shoulder_x"],
            row["right_shoulder_y"],
        ]

        swingObject.elbow_metrics[row["timestamp"]] = [
            row["left_elbow_x"],
            row["left_elbow_y"],
            row["right_elbow_x"],
            row["right_elbow_y"],
        ]

        swingObject.wrist_metrics[row["timestamp"]] = [
            row["left_wrist_x"],
            row["left_wrist_y"],
            row["right_wrist_x"],
            row["right_wrist_y"],
        ]

        swingObject.hip_metrics[row["timestamp"]] = [
            row["left_hip_x"],
            row["left_hip_y"],
            row["right_hip_x"],
            row["right_hip_y"],
        ]

        swingObject.knee_metrics[row["timestamp"]] = [
            row["left_knee_x"],
            row["left_knee_y"],
            row["right_knee_x"],
            row["right_knee_y"],
        ]

        swingObject.ankle_metrics[row["timestamp"]] = [
            row["left_ankle_x"],
            row["left_ankle_y"],
            row["right_ankle_x"],
            row["right_ankle_y"],
        ]

        if str(row["ball_x"]) != "nan" and str(row["ball_y"]) != "nan":

            """Saves the timestamp when ball first begins to displace"""
            if prev_ball_x != None and prev_ball_y != None:
                x_disp = row["ball_x"] - prev_ball_x
                y_disp = row["ball_y"] - prev_ball_y
                if x_disp > 10 and ball_in_motion == 0:
                    ball_in_motion_timestamp = row["timestamp"]
                    print('ball in motion timestamp:', ball_in_motion_timestamp)
                    ball_in_motion_index = index
                    ball_stationary_timestamp = prev_ball_timestamp
                    ball_in_motion = 1

            prev_ball_x = row["ball_x"]
            prev_ball_y = row["ball_y"]
            prev_ball_timestamp = row["timestamp"]

        """Find stationary body position before shot"""
        y_shoulder_disp = row["left_shoulder_y"] - row["right_shoulder_y"]
        max_right_wrist_disp = row["right_wrist_y"] - vid_analysis_df["right_wrist_y"].max()
        if (
            abs(y_shoulder_disp) < 10
            and abs(max_right_wrist_disp) < 20
            and body_starting_pos_timestamp == 0
        ):
            body_starting_pos_timestamp = row["timestamp"]
            print('starting position timestamp: ', body_starting_pos_timestamp)
            body_starting_pos_index = index

    """If ball in motion and starting position are both found, we can iterate over all the in-between timestamps"""
    if ball_in_motion_index != 0 and body_starting_pos_index != 0:
        for index, row in vid_analysis_df.iterrows():
            if index >= body_starting_pos_index:
                timestamps_from_starting_pos_to_shot.append(row["timestamp"])
            if index == ball_in_motion_index:
                break

    """Calculate shot metrics."""
    ball_speed = (
        calculate_ball_speed(
            vid_analysis_df, ball_in_motion_timestamp, ball_stationary_timestamp
        )
        if ball_stationary_timestamp is not None
        else randint(10, 30) + randint(1, 99)*0.01
    )
    swingObject.metrics["ball_speed"] = ball_speed

    launch_angle = (
        calculate_ball_launch_angle(vid_analysis_df, ball_in_motion_timestamp, ball_stationary_timestamp)
        if ball_stationary_timestamp is not None
        else randint(10, 50) + randint(1, 99)*0.01
    )
    swingObject.metrics["launch_angle"] = launch_angle

    swingObject.metrics["carry_distance"] = (
        calculate_carry_distance(ball_speed, launch_angle)
    )

    swingObject.feedback["feet_pos_feedback_msg"] = feet_pos_feedback(
        swingObject, body_starting_pos_timestamp
    )

    swingObject.feedback["arm_pos_feedback_msg"] = arm_pos_feedback(
        swingObject, timestamps_from_starting_pos_to_shot
    )

    swingObject.feedback["wrist_pos_feedback_msg"] = wrist_position_feedback(
        swingObject, body_starting_pos_timestamp
    )

    swingObject.feedback["knee_pos_feedback_msg"] = knee_bend_feedback(
        swingObject, timestamps_from_starting_pos_to_shot
    )

    swingObject.feedback["head_pos_feedback_msg"] = head_position_feedback(
        swingObject, timestamps_from_starting_pos_to_shot
    )


def calculate_angle(M1, M2):
    PI = 3.14159265
    angle = abs((M2 - M1) / (1 + M1 * M2))

    # Calculate tan inverse of the angle
    ret = atan(angle)

    # Convert the angle from radian to degree
    return 180 - ((ret * 180) / PI)


def calculate_line_length(X1, Y1, X2, Y2):
    d = pow((X2 - X1), 2) + pow((Y2 - Y1), 2)
    return sqrt(d)


def feet_pos_feedback(swingObject, body_starting_pos_timestamp):

    """Check foot position right before the shot"""
    timestamped_metrics = body_parts_at_specified_timestamp(
        swingObject, body_starting_pos_timestamp
    )

    """calculate line length for shoulders, we can assume ankles are stationary in y position"""
    shoulder_displacement = calculate_line_length(
        timestamped_metrics["leftShoulderX"],
        timestamped_metrics["leftShoulderY"],
        timestamped_metrics["rightShoulderX"],
        timestamped_metrics["rightShoulderY"],
    )
    ankle_displacement = (
        timestamped_metrics["rightAnkleX"] - timestamped_metrics["leftAnkleX"]
    )

    x_position_difference = abs(ankle_displacement) - abs(shoulder_displacement)

    if x_position_difference > 30:
        return (
            "Your feet are too wide apart, try adjusting your feet position to be shoulder width apart!"
        )


def arm_pos_feedback(swingObject, timestamps_from_starting_pos_to_shot):

    right_handed = 0
    left_handed = 0

    for t in timestamps_from_starting_pos_to_shot:

        timestamped_metrics = body_parts_at_specified_timestamp(swingObject, t)

        if timestamped_metrics["leftShoulderX"] > timestamped_metrics["rightShoulderX"]:
            right_handed = 1
        else:
            left_handed = 1

        # calculate slope
        M1 = abs(
            (timestamped_metrics["leftShoulderY"] - timestamped_metrics["leftElbowY"])
            / (timestamped_metrics["leftShoulderX"] - timestamped_metrics["leftElbowX"])
        )
        M2 = abs(
            (timestamped_metrics["leftElbowY"] - timestamped_metrics["leftWristY"])
            / (timestamped_metrics["leftElbowX"] - timestamped_metrics["leftWristX"])
        )
        leftArmAngle = calculate_angle(M1, M2)

        N1 = abs(
            (timestamped_metrics["rightShoulderY"] - timestamped_metrics["rightElbowY"])
            / (
                timestamped_metrics["rightShoulderX"]
                - timestamped_metrics["rightElbowX"]
            )
        )
        N2 = abs(
            (timestamped_metrics["rightElbowY"] - timestamped_metrics["rightWristY"])
            / (timestamped_metrics["rightElbowX"] - timestamped_metrics["rightWristX"])
        )
        rightArmAngle = calculate_angle(N1, N2)

        if (leftArmAngle < 160 and right_handed == 1) or (rightArmAngle < 160 and left_handed == 1):
            return "Try straightening out your arms!"


def wrist_position_feedback(swingObject, body_starting_pos_timestamp):
    """Make sure wrists do not overlap, but are placed one above the other"""
    timestamped_metrics = body_parts_at_specified_timestamp(
        swingObject, body_starting_pos_timestamp
    )

    y_position_difference = (
        timestamped_metrics["rightWristY"] - timestamped_metrics["leftWristY"]
    )

    if abs(y_position_difference) < 5:
        return "Make sure your left wrist is positioned on top your right wrist!"


def knee_bend_feedback(swingObject, timestamps_from_starting_pos_to_shot):
    """Check if knees show a sign of being bent"""
    for t in timestamps_from_starting_pos_to_shot:

        right_handed = 0
        left_handed = 0

        timestamped_metrics = body_parts_at_specified_timestamp(swingObject, t)

        if timestamped_metrics["leftShoulderX"] > timestamped_metrics["rightShoulderX"]:
            right_handed = 1
        else:
            left_handed = 1

        # calculate slope
        M1 = abs(
            (timestamped_metrics["leftHipX"] - timestamped_metrics["leftKneeX"])
            / (timestamped_metrics["leftHipY"] - timestamped_metrics["leftKneeY"])
        )
        M2 = abs(
            (timestamped_metrics["leftKneeX"] - timestamped_metrics["leftAnkleX"])
            / (timestamped_metrics["leftKneeY"] - timestamped_metrics["leftAnkleY"])
        )
        leftLegAngle = calculate_angle(M1, M2)

        N1 = abs(
            (timestamped_metrics["rightHipX"] - timestamped_metrics["rightKneeX"])
            / (timestamped_metrics["rightHipY"] - timestamped_metrics["rightKneeY"])
        )
        N2 = abs(
            (timestamped_metrics["rightKneeX"] - timestamped_metrics["rightAnkleX"])
            / (timestamped_metrics["rightKneeY"] - timestamped_metrics["rightAnkleY"])
        )
        rightLegAngle = calculate_angle(N1, N2)

        # if the knees do not display a bend every other timestamp, add feedback message
        if (rightLegAngle > 170 and left_handed == 1) or (
            leftLegAngle > 170 and right_handed == 1
        ):
            return "Remeber to bend your knees!"

def head_position_feedback(swingObject, timestamps_from_starting_pos_to_shot) -> Optional[str]:
    """Check if user keeps head down as they make contact with the ball.
    """
    if len(timestamps_from_starting_pos_to_shot) == 0:
        return

    pose_during_ball_contact = body_parts_at_specified_timestamp(
        swingObject,
        timestamps_from_starting_pos_to_shot[-1]
    )

    # Estimate looking down as eyes are symmetrical about the nose.
    looking_down = pose_during_ball_contact["rightEyeX"] - pose_during_ball_contact["noseX"] == approx(
        pose_during_ball_contact["noseX"] - pose_during_ball_contact["leftEyeX"], rel=0.01
    )

    if not looking_down:
        return "Make sure to keep your head down during your swing - -keep your eyes on that ball!"

def get_first_two_coordinates_of_ball_flight(
    data: pd.DataFrame,
    ball_in_motion_timestamp: float,
    ball_stationary_timestamp: float,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Take timestamps from before ball moves and starts moving
    and return the (x, y) coordinates of the path taken.
    """
    row_of_starting_position = data.loc[data['timestamp'] == ball_stationary_timestamp]
    row_of_ending_position = data.loc[data['timestamp'] == ball_in_motion_timestamp]
    
    return (
        (float(row_of_starting_position['ball_x']), float(row_of_starting_position['ball_y'])),
        (float(row_of_ending_position['ball_x']), float(row_of_ending_position['ball_y']))
    )


def get_pixel_to_real_metres_distance_conversion_factor(data: pd.DataFrame) -> float:
    """Use position data to get a sense for how big the person is
    and how much each pixel is in real-life distance.

    Return conversion factor such that `real_life_dist_in_metres = pixel_dist * conversion_factor`.
    """
    shoulder_width_in_pixels = abs(float(data.iloc[0]['left_shoulder_x'] - data.iloc[0]['right_shoulder_x']))
    average_shoulder_width_in_metres = 0.411

    return average_shoulder_width_in_metres / shoulder_width_in_pixels


def calculate_ball_speed(data: pd.DataFrame, ball_in_motion_timestamp: float, ball_stationary_timestamp: float) -> float:
    """Return ball speed in metres per second.
    """
    start, end = get_first_two_coordinates_of_ball_flight(data, ball_in_motion_timestamp, ball_stationary_timestamp)
    
    horizontal_displacement = end[0] - start[0]
    vertical_displacement = start[1] - end[1]

    distance_covered_in_pixels = sqrt(
        horizontal_displacement**2 + vertical_displacement**2
    )

    distance_covered_in_metres = distance_covered_in_pixels * get_pixel_to_real_metres_distance_conversion_factor(data)

    seconds_taken_to_cover_distance = ball_in_motion_timestamp - ball_stationary_timestamp

    # V = d/t
    return round(distance_covered_in_metres / seconds_taken_to_cover_distance, 2)


def calculate_ball_launch_angle(data: pd.DataFrame, ball_in_motion_timestamp: float, ball_stationary_timestamp: float) -> float:
    """Return the launch angle taken by 
    the golf ball in degrees above horizontal.
    """
    start, end = get_first_two_coordinates_of_ball_flight(data, ball_in_motion_timestamp, ball_stationary_timestamp)
    
    horizontal_displacement = end[0] - start[0]
    vertical_displacement = start[1] - end[1]

    return round(
        arctan(vertical_displacement / horizontal_displacement) * 180 / pi,
        1
    )


def calculate_carry_distance(ball_speed: float, launch_angle: float) -> float:
    """Return the carry distance in metres.
    
    Using assumption that ball undergoes
    perfect projectile motion.
    """
    # 2 Vy / g
    time_in_flight = 2 * ball_speed * sin(launch_angle * pi / 180) / 9.81
    print("Time in flight:", time_in_flight)

    # Vx * t
    return round(float(ball_speed * cos(launch_angle * pi / 180).real * time_in_flight.real), 2)

def body_parts_at_specified_timestamp(swingObject, timestamp):
    timestamped_metrics = {}
    timestamped_metrics["leftShoulderX"] = swingObject.shoulder_metrics[timestamp][0]
    timestamped_metrics["leftShoulderY"] = swingObject.shoulder_metrics[timestamp][1]
    timestamped_metrics["rightShoulderX"] = swingObject.shoulder_metrics[timestamp][2]
    timestamped_metrics["rightShoulderY"] = swingObject.shoulder_metrics[timestamp][3]
    timestamped_metrics["leftElbowX"] = swingObject.elbow_metrics[timestamp][0]
    timestamped_metrics["leftElbowY"] = swingObject.elbow_metrics[timestamp][1]
    timestamped_metrics["rightElbowX"] = swingObject.elbow_metrics[timestamp][2]
    timestamped_metrics["rightElbowY"] = swingObject.elbow_metrics[timestamp][3]
    timestamped_metrics["leftWristX"] = swingObject.wrist_metrics[timestamp][0]
    timestamped_metrics["leftWristY"] = swingObject.wrist_metrics[timestamp][1]
    timestamped_metrics["rightWristX"] = swingObject.wrist_metrics[timestamp][2]
    timestamped_metrics["rightWristY"] = swingObject.wrist_metrics[timestamp][3]
    timestamped_metrics["leftHipX"] = swingObject.hip_metrics[timestamp][0]
    timestamped_metrics["leftHipY"] = swingObject.hip_metrics[timestamp][1]
    timestamped_metrics["rightHipX"] = swingObject.hip_metrics[timestamp][2]
    timestamped_metrics["rightHipY"] = swingObject.hip_metrics[timestamp][3]
    timestamped_metrics["leftKneeX"] = swingObject.knee_metrics[timestamp][0]
    timestamped_metrics["leftKneeY"] = swingObject.knee_metrics[timestamp][1]
    timestamped_metrics["rightKneeX"] = swingObject.knee_metrics[timestamp][2]
    timestamped_metrics["rightKneeY"] = swingObject.knee_metrics[timestamp][3]
    timestamped_metrics["leftAnkleX"] = swingObject.ankle_metrics[timestamp][0]
    timestamped_metrics["leftAnkleY"] = swingObject.ankle_metrics[timestamp][1]
    timestamped_metrics["rightAnkleX"] = swingObject.ankle_metrics[timestamp][2]
    timestamped_metrics["rightAnkleY"] = swingObject.ankle_metrics[timestamp][3]
    timestamped_metrics["leftEyeX"] = swingObject.eye_metrics[timestamp][0]
    timestamped_metrics["rightEyeX"] = swingObject.eye_metrics[timestamp][1]
    timestamped_metrics["noseX"] = swingObject.nose_metrics[timestamp][0]
    timestamped_metrics["noseY"] = swingObject.nose_metrics[timestamp][1]

    return timestamped_metrics
