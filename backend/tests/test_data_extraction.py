'''
Use sample image/video frames to test data extraction, 
including detecting the coordinates of the golf ball and 
player position information.
'''

from data_extraction.ball_detection import get_coordinates_of_golf_ball_in_image

import cv2
import pytest

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