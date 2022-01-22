'''
Sample script to detect the location of a 
golf ball in a video clip and compute some basic metrics.
'''

import time
from typing import List, Generator, Any, Tuple, Optional
from enum import Enum

import cv2
import numpy as np

Image = Any

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

    # Apply Gaussian blur and colour masking
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.inRange(image, (180, 180, 180), (255,255,255))
    image = cv2.bitwise_not(image)

    # Run blob detection, filtering on circularity and color.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = True
    params.minCircularity = 0.9
    params.blobColor = 0
    detector = cv2.SimpleBlobDetector_create(parameters=params)
    keypoints = detector.detect(image)

    # Return either the found coordinates or None, None
    if keypoints:
        return keypoints[0].pt
    return None, None
