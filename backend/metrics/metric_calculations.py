'''
Use image detection to generate Dataframe of corresponding data points. Ball, club, body positions will be tracked. 
This file will generate some dummy data for these positions and perform the calculations to track metrics.
'''

## dummy data for ball position with timestamp 
import pandas as pd
ball_position_data = [
    [0.0, 405, 532, 'NULL', 'NULL'],
    [0.03, 405, 532, 'NULL', 'NULL'],
    [0.06, 405, 532, 'NULL', 'NULL'],
    [0.09, 405, 532, 'NULL', 'NULL'],
    [0.12, 405, 532, 171.536, 441.05],
    [0.15, 405, 532, 171.536, 441.05],
    [0.18, 405, 532, 171.536, 441.05],
    [0.84, 405, 532, 171.536, 441.05],
    [0.87, 405, 532, 171.536, 441.05],
    [0.9, 405, 532, 171.536, 441.05],
    [0.30, 405, 532, 171.536, 441.05],
    [1.08, 405, 532, 171.536, 441.05],
    [1.11, 405, 532, 171.536, 441.05],
    [1.14, 405, 532, 271.68, 376.94],
    [1.17, 405, 532, 271.68, 376.94],
    [1.2, 405, 532, 344.42, 330.02],
    [1.23, 405, 532, 344.42, 330.02],
    [1.26, 405, 532, 344.42, 330.02],
    [1.29, 405, 532, 344.42, 330.02],
    [1.32, 405, 532, 344.42, 330.02],
    [1.35, 405, 532, 344.42, 330.02],
    [1.38, 405, 532, 344.42, 330.02]
]

ball_pos_df = pd.DataFrame(ball_position_data, columns= ['timestamp', 'video_width', 'video_height', 'ball_x', 'ball_y'])
#print(ball_pos_df)

# calculate ball speed

# calculate launch angle (just gonna assume ground y position is 20 pixels lower than ball position)

body_pos_df = pd.read_csv ('body_position_data.csv')
#print(body_pos_df)

# check if position of feet is within a certain range of shoulder position 
right_shoulder_x = body_pos_df.loc[:, 'right_shoulder_x']
left = body_pos_df.loc[:, 'left_shoulder_x']

right_ankle_x = body_pos_df.loc[:, 'right_ankle_x']
left_ankle_x = body_pos_df.loc[:, 'left_ankle_x']


# are x and y values switched for this? data doesnt make much sense, getting negatives
for index, row in body_pos_df.iterrows():
    right_shoulder_x = row['right_shoulder_x']
    left_shoulder_x = row['left_shoulder_x']
    right_ankle_x = row['right_ankle_x']
    left_ankle_x = row['left_ankle_x']

    shoulder_diff = right_shoulder_x - left_shoulder_x
    ankle_diff = right_ankle_x - left_ankle_x
    print(shoulder_diff, ankle_diff)

    #print(row['right_shoulder_x'], row['left_shoulder_x'])




