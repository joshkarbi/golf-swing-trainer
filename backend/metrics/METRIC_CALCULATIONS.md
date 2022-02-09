## List of metrics as well as corresponding calculations ##

We will be using pandas.DataFrame to track the metrics in the video. The DataFrame will contain various data points such as ball_x, ball_y, left_shoulder_x, left_shoulder_y etc.  

### Required data points ###
- Ball position(x,y)
- Club head position
  - Top and bottom of head which hits ball (x,y)
  - Back of club pointed position (x,y)
- Ground position (x,y)
  - needed for launch angle, carry distance 
- Shoulder and elbow positions (left, right, x, y)
  - Be able to tell the user to straighten arms if they are bent
- Knee positions (x,y)
  - Be able to detect if the person is standing stright or in a squat

### desired metrics ###
- Ball speed (velocity of ball just after impact)
- Club speed (the club head's velocity just prior to the club's impact with the ball)
- Smash factor (ball speed/club speed)
- Launch angle (angle of ball relative to ground after its been hit)
- Carry distance (how far the ball travels before hitting the ground)
- Angle of attack (vertical angle of clubhead at impact)
- Dynamic loft (angle between angle of attack and launch angle)

### Calculations ###
- **Ball speed:** 
  - use all ball_x and ball_y values from DataFrame as well as their timestamps to determine ball speed
  - once ball positions start drasticlally changing (to avoid noise) record first few points
- **Club speed:** 
  - use last few club_x and club_y values to determine club head velocity prior to ball impact
  - use values before drastic ball movement is recorded 
- **Smash factor:** 
  - use ball speed and club speed to determine smash factor.
- **Launch angle:**
  - use average of first few ball_x ball_y positions to calculate angle relative to ground after impact
  - x,y values of ground 
- **Carry distance:** 
  - position x right when ball starts moving, position x of ball right when it hits ground 

### Problems??? ###
- Will the club head be difficult to detect with added noise? In which case will we be able to determine the angle of attack? 
- Can we have two video types to upload, one for the body position from afar and one for the close up of the shot
  - far video will be able to give feedback about body position?
- Carry distance we can't keep track of because we won't know when the ball hits the ground 

