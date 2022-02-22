'''
Use image detection to generate Dataframe of corresponding data points. Ball, club, body positions will be tracked. 
This file will generate some dummy data for these positions and perform the calculations to track metrics.

    X and Y coordinates are distances from top left corner of the image
    going rightward and downward, respectively, in pixels.

'''

from sqlite3 import Timestamp
from typing import NamedTuple
import pandas as pd
from math import atan

class GolfSwingFeedbackInfoAndMetrics(NamedTuple):
    ball_speed: int
    launch_angle: int

    '''Body Position Feedback:
        each incorrect body position will have written feedback for what to change 
        ex. arm position bad, tuck elbows in
    '''
    #shoulder_feet_pos_success: bool
    feet_pos_feedback: str
    shoulder_metrics={}
    elbow_metrics={}
    wrist_metrics={}
    hip_metrics={}
    knee_metrics={}
    ankle_metrics={}
    
    #arm_pos_success: bool
    arm_pos_feedback: str

vid_analysis_df = pd.read_csv('data_extraction.csv')

def analyze_datapoints(vid_analysis_df) -> pd.DataFrame:
    '''Input is the csv generated from video analysis,
    output will result in df including metrics, and feedback for body positions 
    TODO: score shot based on quality of feedback acchieved'''

    feedback = []
    calculation_metrics = []
    metrics = GolfSwingFeedbackInfoAndMetrics(10, 10, '', '')
    prev_ball_x = None
    prev_ball_y = None
    prev_ball_timestamp = 0
    ball_in_motion = 0

    for index, row in vid_analysis_df.iterrows():

        metrics.shoulder_metrics[row['timestamp']] =[row['left_shoulder_x'],
                                                row['left_shoulder_y'],
                                                row['right_shoulder_x'],
                                                row['right_shoulder_y']]

        metrics.elbow_metrics[row['timestamp']] =[row['left_elbow_x'],
                                                row['left_elbow_y'],
                                                row['right_elbow_x'],
                                                row['right_elbow_y']]

        metrics.wrist_metrics[row['timestamp']] =[row['left_wrist_x'],
                                                row['left_wrist_y'],
                                                row['right_wrist_x'],
                                                row['right_wrist_y']]

        metrics.hip_metrics[row['timestamp']] =[row['left_hip_x'],
                                                row['left_hip_y'],
                                                row['right_hip_x'],
                                                row['right_hip_y']]

        metrics.knee_metrics[row['timestamp']] =[row['left_knee_x'],
                                                row['left_knee_y'],
                                                row['right_knee_x'],
                                                row['right_knee_y']]

        metrics.ankle_metrics[row['timestamp']] =[row['left_ankle_x'],
                                                row['left_ankle_y'],
                                                row['right_ankle_x'],
                                                row['right_ankle_y']]

        if str(row['ball_x']) != 'nan' and str(row['ball_y']) != 'nan':
        
            '''Saves the timestamp when ball first begins to displace'''
            if prev_ball_x !=None and prev_ball_y !=None:
                x_disp = row['ball_x'] - prev_ball_x
                y_disp = row['ball_y'] - prev_ball_y
                if x_disp > 10 and y_disp < 10 and ball_in_motion == 0:
                    ball_in_motion_timestamp = row['timestamp']
                    #ball_in_motion_index = index
                    ball_stationary_timestamp = prev_ball_timestamp
                    ball_in_motion = 1

            prev_ball_x = row['ball_x']
            prev_ball_y = row['ball_y']
            prev_ball_timestamp = row['timestamp']


    '''TODO: ball speed calculation'''
    ball_speed = ball_speed_calculation(metrics, ball_in_motion_timestamp, ball_stationary_timestamp)

    '''TODO: launch angle calculation, also get ground position'''
    launch_angle = launch_angle_calculation(ball_speed, 445)

    '''TODO: shoulder position calculation'''
    feet_pos_feedback_msg = feet_pos_feedback(metrics, ball_in_motion_timestamp, ball_stationary_timestamp)

    arm_pos_feedback_msg = arm_pos_feedback(metrics, ball_in_motion_timestamp, ball_stationary_timestamp)

    # metrics.ball_speed = ball_speed
    # metrics.launch_angle = launch_angle
    # metrics.feet_pos_feedback = feet_pos_feedback
    # metrics.arm_pos_feedback = arm_pos_feedback

    # figure out how to send object as a dataframe, unless we just want to send an object? 
    # res = pd.DataFrame(metrics)
    # res.to_csv("golf_swing_feedback.csv", na_rep='NULL')
    # return res

def calculate_angle(M1,M2):
    PI = 3.14159265
    angle = abs((M2 - M1) / (1 + M1 * M2))

    # Calculate tan inverse of the angle
    ret = atan(angle)

    # Convert the angle from radian to degree
    return((ret * 180) / PI)


def ball_speed_calculation(calculation_metrics, ball_in_motion_timestamp, ball_stationary_timestamp):
    '''Return ball speed, reference to timestamp of the ball before and immediately after impact
        TODO: calculate ball speed 
    '''
    return 10

def launch_angle_calculation(ball_speed, ground_pos):
    '''Launch Angle Calculation
        angle of ball relative to ground after its been hit
        for now just estimate ground position (x amount of pixels lower than ball)
        TODO: actual calc for ball speed
    '''
    return 10

def feet_pos_feedback(metrics, ball_in_motion_timestamp, ball_stationary_timestamp): 

    '''check if position of feet is outside a range of shoulder position, can provide feedback if feet are too wide
        ref: https://www.golfdistillery.com/swing-tips/setup-address/feet-position/'''
    
    '''Check foot position right before the shot'''
    time_stamp = ball_stationary_timestamp

    leftAnkleX = metrics.ankle_metrics[time_stamp][0]
    leftAnkleY = metrics.ankle_metrics[time_stamp][1]
    rightAnkleX = metrics.ankle_metrics[time_stamp][2]
    rightAnkleY = metrics.ankle_metrics[time_stamp][3]
    leftShoulderX = metrics.shoulder_metrics[time_stamp][0]
    leftShoulderY=metrics.shoulder_metrics[time_stamp][1]
    rightShoulderX=metrics.shoulder_metrics[time_stamp][2]
    rightShoulderY=metrics.shoulder_metrics[time_stamp][3]

    print('ankle positions: ', leftAnkleX, leftAnkleY, rightAnkleX, rightAnkleY)
    print('shoulder positions: ', leftShoulderX, leftShoulderY, rightShoulderX, rightShoulderY)




def arm_pos_feedback(metrics, ball_in_motion_timestamp, ball_stationary_timestamp):
    
    'first lets focus on getting measurements just before ball impact'
    time_stamp=ball_stationary_timestamp
    leftShoulderX = metrics.shoulder_metrics[time_stamp][0]
    leftShoulderY=metrics.shoulder_metrics[time_stamp][1]
    rightShoulderX=metrics.shoulder_metrics[time_stamp][2]
    rightShoulderY=metrics.shoulder_metrics[time_stamp][3]
    leftElbowX=metrics.elbow_metrics[time_stamp][0]
    leftElbowY=metrics.elbow_metrics[time_stamp][1]
    rightElbowX=metrics.elbow_metrics[time_stamp][2]
    rightElbowY=metrics.elbow_metrics[time_stamp][3]
    leftHandX=metrics.wrist_metrics[time_stamp][0]
    leftHandY=metrics.wrist_metrics[time_stamp][1]
    rightHandX=metrics.wrist_metrics[time_stamp][2]
    rightHandY=metrics.wrist_metrics[time_stamp][3]


    #calculate slope
    M1 = abs((leftShoulderX-leftElbowX)/(leftShoulderY-leftElbowY))
    M2 = abs((leftElbowX-leftHandX)/(leftElbowY-leftHandY))
    leftArmAngle = calculate_angle(M1,M2)
    
    N1 = abs((rightShoulderX-rightElbowX)/(rightShoulderY-rightElbowY))
    N2 = abs((rightElbowX-rightHandX)/(rightShoulderY-rightHandY))
    rightArmAngle = calculate_angle(N1,N2)

    #print(leftArmAngle)
    #if the arm isn't straight enough, add to feedback message
    if(leftArmAngle < 170 or rightArmAngle < 170 ):
        #TODO: append a feedback message
        print('temp')

def knee_pos_feedback(metrics, ball_in_motion_timestamp, ball_stationary_timestamp):
    '''Check if players knees are bent appropriately'''
    time_stamp=ball_stationary_timestamp
    hipsX = metrics.hip_metrics[time_stamp][0]
    hipsY = metrics.hip_metrics[time_stamp][1]
    kneesX=metrics.knee_metrics[time_stamp][0]
    kneesY=metrics.knee_metrics[time_stamp][1]
    feetX = metrics.feet_metrics[time_stamp][0]
    feetY = metrics.feet_metrics[time_stamp][1]
    M1 = abs((hipsX-kneesX)/(hipsY-kneesY))
    M2 = abs((kneesX-feetX)/(kneesY-feetY))
    kneeAngle = calculate_angle(M1,M2)

    # if(kneeAngle<170):
    #     #TODO: append feedback message for knee angle

def shoulder_motion_feedback(calculation_metrics, ball_in_motion_timestamp, ball_stationary_timestamp):
    '''Check motion of shoulders during golf swing'''

analyze_datapoints(vid_analysis_df)