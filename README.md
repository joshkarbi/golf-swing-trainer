# golf-swing-trainer #
A mobile app that analyzes user golf swings and provides advice on how to improve their swing, as well as some shot metrics to help them track their progress.

## App Screenshots ##

<img src="/docs/app_screenshots.png" width="600" />

## Swing Analysis Visualization ##

<p float="left">
  <img src="/docs/swing.gif" width="200" />
  <img src="/docs/computer_vision.gif" width="200" /> 
  <img src="/docs/animation.gif" width="200" />
</p>

## App ##
Built using Flutter. Can be loaded onto an Android or iOS device following Flutter documentation.

## Backend ##
Built using Python and TensorFlow MoveNet for pose estimation, OpenCV for golf ball tracking, and Flask for server capabilities.

### Directory Structure ###

    .
    ├── archive                   # Old code that might be useful at some point.
    ├── assets                    # Sample images/videos used to test the system.
    ├── data_extraction           # Module providing functionality to extract data out of video/images (i.e. golf ball coordinates, player positioning).
    ├── metrics                   # Module responsible for swing metric calculations and feedback generation.
    ├── static                    # Used by application.
    └── tests                     # Unit tests.

### How do I get setup? ###
- Have Python 3.8 or 3.9 installed.
- Install poetry: https://python-poetry.org/docs/
- Create a virtual environment: `virtualenv env/`
- Activate the virtual environment: `source env/bin/activate` (on Linux) or `.\env\Scripts\activate` (on Windows)
- Install dependencies: `poetry install`
- Run the server: `flask run --host=0.0.0.0 --port=5000`
