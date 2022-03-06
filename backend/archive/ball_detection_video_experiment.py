import cv2
import numpy as np
import imageio

ball_key_points = []


def track_ball(im):
    global ball_key_points
    original_frame = im

    im = cv2.GaussianBlur(im, (3, 3), 0)
    im = cv2.inRange(im, (180, 180, 180), (255, 255, 255))
    im = cv2.bitwise_not(im)

    ### BLOB DETECTION ###

    params = cv2.SimpleBlobDetector_Params()

    params.filterByCircularity = True
    params.minCircularity = 0.9

    # params.minThreshold = 250
    # params.maxThreshold = 255
    # params.minRepeatability = 1
    params.blobColor = 0
    detector = cv2.SimpleBlobDetector_create(parameters=params)
    keypoints = detector.detect(im)

    if keypoints and keypoints[0].pt[1] < len(im) / 2:
        keypoints = None
    # Keep track of ball points over time so we can draw the path
    if keypoints:
        print("Ball at", keypoints[0].pt)
        ball_key_points.append(keypoints)
    for key_point in ball_key_points:
        print("drawing", key_point[0].pt)
        original_frame = cv2.drawKeypoints(
            original_frame,
            key_point,
            np.array([]),
            (0, 0, 255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        )

    return original_frame


### CREATE MASK OF IMAGE HIGHLIGHTING WHITE/GRAY REGIONS ###

vid_capture = cv2.VideoCapture("assets/samples-josh/004.mp4")
frame_width = int(vid_capture.get(3))
frame_height = int(vid_capture.get(4))
frame_size = (frame_width, frame_height)
fps = vid_capture.get(cv2.CAP_PROP_FPS)

output_frames = []
while vid_capture.isOpened():
    ret, frame = vid_capture.read()
    if ret:
        frame_with_ball_tracked = track_ball(frame)
        frame_rgb = cv2.cvtColor(frame_with_ball_tracked, cv2.COLOR_BGR2RGB)
        output_frames.append(frame_rgb)
        # cv2.imshow("",output_frames[-1])
        # cv2.waitKey(0)
    else:
        break

vid_capture.release()
imageio.mimsave(
    "assets/samples-josh/004-ball-tracking.mp4", output_frames, fps=fps / 2, format="MP4"
)
