## About ##
This directory contains application and test code for a 
backend processing system for the golf swing trainer app.

## Directory Structure ##

archive/: Old code that might be useful at some point.

assets/: Sample images/videos used to test the system.

data_extraction/: Module providing functionality to extract data out of video/images (i.e. golf ball coordinates, player positioning).

tests/: Unit tests.

## How do I get setup? ##
- Have Python 3.8 or 3.9 installed.
- Install poetry: https://python-poetry.org/docs/
- Create a virtual environment with `virtualenv env/`
- Activate the virtual environment with `source env/bin/activate`
- Install dependencies with `poetry install`

### How do I run the tests? ##
Assuming you're running `python3.8` in your virtualenv:

```bash
python3.8 -m pytest
```

