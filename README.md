# securitycams
ECSE 488 Surveillance System

### 1. Create a virtual environment:

### `python3 -m venv venv`

### 2. Activate the virtual environment:

### `source venv/bin/activate`

### 3. Install the following package in your environment:

### `(venv) $ pip install opencv-python`

### 4. Exit out of the virtual environment. 
To run the code, in the command line paste the following:

### `python3 gui.py`

### 5. Create a folder within the securitycams directory called 'image_captures'. 
This is where the images from the security system will be saved.

### `mkdir image_captures`

### OTHER NOTES:
The camera source for both cameras have been set to 0, but if you have attached another camera, please change the following on line 11 of gui.py:
    
### `cam2_src = 1`


