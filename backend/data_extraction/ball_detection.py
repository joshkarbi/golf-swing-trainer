'''
Sample script to detect the location of a 
golf ball in a video clip and compute some basic metrics.
'''

from typing import List, Generator, Any, Tuple, Optional

import cv2
import numpy as np

def is_pixel_likely_part_of_golf_ball(pixel: List[int]):
    """Determine if a pixel is likely part of a golf ball.
    
    Parameters
    ----------
    pixel: List[int]
        List of R, G, B integer values.
    """
    if sum(pixel) > 650:
        return True

Image = Any
def get_video_frames(video_file_name: str) -> Generator[Image, None, None]:
    """Generator to pull image frames out of a video file.

    Parameters
    ----------
    video_file_name : str
        Name of file.
    """

    vs = cv2.VideoCapture(video_file_name)

    while True:
        is_next_frame, frame = vs.read()
        if is_next_frame:
            yield frame
        else:
            return

def get_coordinates_of_golf_ball_in_image(image: Image) -> Optional[Tuple[int, int]]:
    """Get the (x, y) coordinates of a golf ball in an image.

    X and Y coordinates are distances from top left corner of the image
    going rightward and downward, respectively, in pixels.

    Parameters
    ----------
    image : Image
        Image to pull coordinates out of.

    Returns
    -------
    Optional[Tuple[int, int]]
        (x, y) coordinates of golf ball if detected or None.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect circles in the frame.
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")    
        
        for (x, y, r) in circles:
            if is_pixel_likely_part_of_golf_ball(pixel = image[y, x]):
                return (x, y)
    
def get_sequence_of_golf_ball_locations(video_file_name: str) -> List[Tuple[int, int]]:
    """Analyze a video sequence and determine the series
    of golf ball (x, y) locations.

    Parameters
    ----------
    video_file_name : str
        Name of file to analyze.

    Returns
    -------
    List[Tuple[int, int]]
        List of (x, y) coordinates in the video representing the
        assumed location of the golf ball.

    TODO: Filter out noise (golf ball hasn't really moved but coordinates
    change slightly). This will make metrics inaccurate.
    """

    result = []

    for image in get_video_frames(video_file_name=video_file_name):
        coordinates = get_coordinates_of_golf_ball_in_image(image = image)
        if coordinates:
            result.append(coordinates)

    return result

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def get_smooth_shot_coordinates(ball_coordinates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Get a sequence of coordinates, smoothed with 
    a moving average, representing one shot."""

    # TODO
    return

def get_golf_ball_velocity_angles(ball_coordinates: List[Tuple[int, int]]) -> List[float]:
    """Determine the angle of ball velocity at each point in time.
    First point will have the same result as the 2nd point as there
    is no previous datapoint to compute the angle with.

    Parameters
    ----------
    ball_coordinates : List[Tuple[int, int]]
        Chronological coordinates of the golf ball.

    Returns
    -------
    List[float]
        List, same size as input, containing approximate velocity
        angles at each point in time, in degrees.
    """

    result = [0]
    for previous, current in zip(ball_coordinates, ball_coordinates[1:]):
        x_travelled = current[0] - previous[0] # Expect a smaller x -> larger x
        y_travelled = previous[1] - current[1] # Expect larger y -> smaller y
        
        result.append(
            np.rad2deg(np.arctan(y_travelled / x_travelled))
        )
    
    result[0] = result[1]
    return result

def get_approximated_launch_angle(velocity_angles: List[float]) -> float:
    """Estimate the launch angle from a dirty set
    of velocity angles (includes negative numbers
    and nans from noise, being stationary, etc.)
    """
    valid_measurements = []

    for angle in velocity_angles:
        if angle != np.nan and angle > 0:
            valid_measurements.append(angle)

    return round(np.average(valid_measurements), 2)

def main():
    coordinates = (
        get_sequence_of_golf_ball_locations(
            video_file_name="assets/swing_sample_video.mp4"
        )
    )

    velocity_angles = get_golf_ball_velocity_angles(
        ball_coordinates=coordinates
    )


    for coord, velocity_angle in zip(coordinates, velocity_angles):
        print(
            f"At coordinate {coord} velocity angle was {velocity_angle} degrees."
        )

    print(
        "ESTIMATED LAUNCH ANGLE: ", 
        get_approximated_launch_angle(velocity_angles),
        "degrees."
    )

if __name__=="__main__":
    main()

