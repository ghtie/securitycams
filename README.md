# securitycams
ECSE 488 Surveillance System

## Project Overview
The contents of this zip folder include all of the source code for our surveillance camera system. Our system only utilizes 2 USB cameras. The main file to run our surveillance system is gui.py.

### Gui.py
Runs our surveillance system GUI 

### Video_frames.py
Uses multithreading to retrieve frames from each camera

### Security.py
Runs the backend of our surveillance system 

### Human_detection.py
Loads the human detection model and outputs the model's classification, confidence scores, and detection boxes for humans in images

### Frame_analyzer.py
Analyzes each frame for the following: moving objects, passing humans, and approaching humans. It will save image captures if an approaching human is detected

### Model_test.py
Runs experiments on the human detection model. The accuracy and precision for each test dataset is found in the summary.txt file. The two test datasets used were not included in this zip file because of the size, but are linked below:<br>
    1. https://www.kaggle.com/aliasgartaksali/human-and-non-human <br>
    2. https://www.kaggle.com/bikashjaiswal/dataset-for-mask-nonmask-and-nonhuman-classes <br>

### Summary.txt
Contains the summary of the human detection model experiments.

## Running the Code

### 1. Create a virtual environment:

### `python3 -m venv venv`

### 2. Activate the virtual environment:

### `source venv/bin/activate`

### 3. Install the following package in your environment:

### `(venv) $ pip install opencv-python`

### 4. Exit out of the virtual environment. 
To run the code, in the command line paste the following:

### `python3 gui.py`

### OTHER NOTES:
The camera source for both cameras have been set to 0, but if you have attached another camera, please change the following on line 11 of gui.py:
    
### `cam2_src = 1`


