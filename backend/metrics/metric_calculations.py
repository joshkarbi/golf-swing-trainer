'''
Use image detection to generate Dataframe of corresponding data points. Ball, club, body positions will be tracked. 
This file will generate some dummy data for these positions and perform the calculations to track metrics.

    X and Y coordinates are distances from top left corner of the image
    going rightward and downward, respectively, in pixels.

'''

import pandas as pd
from tomlkit import string

class GolfSwingFeedbackInfoAndMetrics(NamedTuple):
    ball_speed: int
    launch_angle: int

    '''Body Position Feedback:
        each speicific body position will have a true/false for accuracy success
        as well as written feedback for what to change 
        ex. arm position success is false, tuck elbows in
        when returning feedback to user, only messages corresponding to false success will appear
    '''
    shoulder_feet_pos_success: bool
    shoulder_feet_pos_feedback: string

    arm_pos_success: bool
    arm_pos_feedback: string

vid_analysis_df = pd.read_csv('debug_data_extraction.csv')

def analyze_datapoints(vid_analysis_df) -> pd.DataFrame:
    '''
    Input is the csv generated from video analysis,
    output will result in df including metrics, and feedback for body positions 
    TODO: score shot based on quality of feedback acchieved 
    '''
    feedback = []
    ball_speed_metrics = []
    shoulder_feet_pos_metrics = []
    arm_pos_metrics = []


    for index, row in vid_analysis_df.iterrows():

        '''Ball Speed Calculations 
            ball speed corresponds to the speed of the ball after impact
            ball_x, ball_y might be NULL for the first few timestamps, 
            need to determine original position of ball (account for noise)
            as well as when ball starts drastically changing position (in flight)
            gather first few positions and timetamps of ball in impact and estimate speed
            TODO: actual calc for ball speed
        '''

        #append if not null
        ball_speed_metrics.append([row['timestamp'], row['ball_x'],row['ball_y']])

        #once enough points are captured to determine speed, call function
        ball_speed = ball_speed_calculation(ball_speed_metrics)


        '''Launch Angle Calculation
            angle of ball relative to ground after its been hit
            for now just estimate ground position (x amount of pixels lower than ball)
            TODO: actual calc for ball speed
        '''
        ground_pos_y = row['ball_y'] - 20
        launch_angle = launch_angle_calculation(ball_speed, ground_pos_y)


        '''Feet/Shoulder Position Feedback
            four types of feet stances, each corresponds to different shot type:
                - wide (inside of feet align with outside of shoulders)
                - normal (feet and shoulder width equal distance)
                - narrow (outside of feet align with outside of shoulder)
                - very narrow (feet almost toching)

            check if position of feet is outside a range of shoulder position, can provide feedback if feet are too wide
            ref: https://www.golfdistillery.com/swing-tips/setup-address/feet-position/
        '''

        #append position before shot, timestamp of when ball starts moving will be the final metric we need here
        shoulder_feet_pos_metrics.append([row['timestamp'], row['right_shoulder_x'], row['left_shoulder_x'], row['right_ankle_x'], row['left_ankle_x']])

        shoulder_feet_pos_feedback = shoulder_feet_pos_feedback(shoulder_feet_pos_metrics)
    
        '''Arm Position Feedback
            Determine accuracy of arm position (the leading arm in the shot)
            Four main sections:
                - address
                - backswing
                - downswing
                - followthrough
            I guess it's necessary to keep track of most of these positions as the entire swing itself is a constant moevement 
            ref: https://theleftrough.com/right-arm-in-golf-swing/
        '''

        arm_pos_metrics.append([row['timestamp'], row['left_shoulder_x'], row['left_shoulder_y'], row['right_shoulder_x'], row['right_shoulder_y'], 
            row['left_elbow_x'], row['left_elbow_y'], row['right_elbow_x'], row['right_elbow_y'],
            row['left_wrist_x'], row['left_wrist_y'], row['right_wrist_x'], row['right_wrist_y']])
        
        #call this once we have all the arm position metrics we need, just adding here as reference 
        arm_pos_feedback = arm_pos_feedback(arm_pos_metrics)

def ball_speed_calculation(ball_speed_data):
    '''return ball speed '''

def launch_angle_calculation(ball_speed, ground_pos):
    '''return launch angle based on ball speed '''

def shoulder_feet_pos_feedback(pos_data): 
    '''Determine if feet position is satisfactory, return tailored feedback message if not 
        shoulder_diff = right_shoulder_x - left_shoulder_x
        ankle_diff = right_ankle_x - left_ankle_x
    
    '''

def arm_pos_feedback(pos_data):
    '''Determine if arm position is satisfactory, return tailored feedback message if not '''
