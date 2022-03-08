# golf-swing-trainer
An app that analyzes user golf swings and provides useful feedback.

### Demos ##

<p float="left">
  <img src="/docs/swing.gif" width="200" />
  <img src="/docs/computer_vision.gif" width="200" /> 
  <img src="/docs/animation.gif" width="200" />
</p>

### Backend Directory Structure ###

    .
    ├── archive                   # Old code that might be useful at some point.
    ├── assets                    # Sample images/videos used to test the system.
    ├── data_extraction           # Module providing functionality to extract data out of video/images (i.e. golf ball coordinates, player positioning).
    ├── metrics                   # Module responsible for swing metric calculations and feedback generation
    └── tests                     # Unit tests.

### How do I get setup? ###
- Have Python 3.8 or 3.9 installed.
- Install poetry: https://python-poetry.org/docs/
- Create a virtual environment with `virtualenv env/`
- Activate the virtual environment with `source env/bin/activate` (on Linux) or `.\env\Scripts\activate` (on Windows)
- Install dependencies with `poetry install`

#### How do I run the tests? ###
```bash
pytest
```
or (assuming you're running python3.8 in your environment):

```bash
python3.8 -m pytest
```