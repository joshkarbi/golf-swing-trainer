'''
Run pose inference on video frames of a player swinging.
'''

from typing import Any, Dict
import tensorflow as tf
import tensorflow_hub as hub

import cv2

Image = Any

model_name = "movenet_lightning"
module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
input_size = 192

def movenet(input_image):
  """Runs detection on an input image.

  Args:
    input_image: A [1, height, width, 3] tensor represents the input image
      pixels. Note that the height/width should already be resized and match the
      expected input resolution of the model before passing into this function.

  Returns:
    A [1, 1, 17, 3] float numpy array representing the predicted keypoint
    coordinates and scores.
  """
  model = module.signatures['serving_default']

  # SavedModel format expects tensor type of int32.
  input_image = tf.cast(input_image, dtype=tf.int32)

  # Run model inference.
  outputs = model(input_image)
  
  # Output is a [1, 1, 17, 3] tensor.
  keypoints_with_scores = outputs['output_0'].numpy()
  return keypoints_with_scores


def init_crop_region(image_height, image_width):
  """Defines the default crop region.

  The function provides the initial crop region (pads the full image from both
  sides to make it a square image) when the algorithm cannot reliably determine
  the crop region from the previous frame.
  """
  if image_width > image_height:
    box_height = image_width / image_height
    box_width = 1.0
    y_min = (image_height / 2 - image_width / 2) / image_height
    x_min = 0.0
  else:
    box_height = 1.0
    box_width = image_height / image_width
    y_min = 0.0
    x_min = (image_width / 2 - image_height / 2) / image_width

  return {
    'y_min': y_min,
    'x_min': x_min,
    'y_max': y_min + box_height,
    'x_max': x_min + box_width,
    'height': box_height,
    'width': box_width
  }


def crop_and_resize(image, crop_region, crop_size):
  """Crops and resize the image to prepare for the model input."""
  boxes=[[crop_region['y_min'], crop_region['x_min'],
          crop_region['y_max'], crop_region['x_max']]]
  output_image = tf.image.crop_and_resize(
      image, box_indices=[0], boxes=boxes, crop_size=crop_size)
  return output_image


def run_inference(movenet, image, crop_region, crop_size):
  """Runs model inferece on the cropped region.

  The function runs the model inference on the cropped region and updates the
  model output to the original image coordinate system.
  """
  image_height, image_width, _ = image.shape
  input_image = crop_and_resize(
    tf.expand_dims(image, axis=0), crop_region, crop_size=crop_size)
  # Run model inference.
  keypoints_with_scores = movenet(input_image)

  # Update the coordinates.
  for idx in range(17):
    keypoints_with_scores[0, 0, idx, 0] = (
        crop_region['y_min'] * image_height +
        crop_region['height'] * image_height *
        keypoints_with_scores[0, 0, idx, 0]) / image_height
    keypoints_with_scores[0, 0, idx, 1] = (
        crop_region['x_min'] * image_width +
        crop_region['width'] * image_width *
        keypoints_with_scores[0, 0, idx, 1]) / image_width
  return keypoints_with_scores

BodyPartLabel = str
PixelCoordinate = float
def get_body_part_positions_in_image(image: Image) -> Dict[BodyPartLabel, PixelCoordinate]:
  """Run MoveNet inference on an image frame
  and return body part positions.
  """

  image_height, image_width, _ = image.shape
  crop_region = init_crop_region(image_height, image_width)
  keypoints_with_scores = run_inference(
    movenet=movenet,
    image=image,
    crop_region=crop_region,
    crop_size=[input_size, input_size]
  )

  res = {}

  for keypoints, labels in zip(
    keypoints_with_scores[0][0],
    ['nose','left_eye','right_eye','left_ear','right_ear','left_shoulder','right_shoulder','left_elbow','right_elbow',
    'left_wrist','right_wrist', 'left_hip','right_hip','left_knee','right_knee','left_ankle','right_ankle']
  ):
    res[labels+"_x"] = round(keypoints[1] * image_width, 2)
    res[labels+"_y"] = round(keypoints[0] * image_height, 2)

  return res

