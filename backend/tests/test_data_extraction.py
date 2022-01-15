'''
Use sample image/video frames to test data extraction, 
including detecting the coordinates of the golf ball and 
player position information.
'''

from data_extraction.ball_detection import get_coordinates_of_golf_ball_in_image

import cv2
import pytest

def test_ball_detection_1():
    """Test using an 852 x 480 image.

    Ball is approximately 54% across horizontally 
    and 44% down (calculated manually).
    """
    test_image = cv2.imread("assets/ball_close_up.jpg")
    
    x, y = get_coordinates_of_golf_ball_in_image(
        test_image
    )
    
    # Check the detected coordinates are within 1.5% of expected.
    assert x == pytest.approx(0.54 * 852, rel=0.015)
    assert y == pytest.approx(0.44 * 480, rel=0.015)


def test_ball_detection_2():
    """Test using an 731 x 1024 image.

    Ball is approximately 62.1% across horizontally 
    and 85.5% down (calculated manually).
    """
    test_image = cv2.imread("assets/player_swinging_2.jpg")
    
    breakpoint()
    x, y = get_coordinates_of_golf_ball_in_image(
        test_image
    )
    
    # Check the detected coordinates are within 1.5% of expected.
    assert x == pytest.approx(0.621 * 731, rel=0.015)
    assert y == pytest.approx(0.855 * 1024, rel=0.015)