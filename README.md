# Image Processing App

A GUI-based application for extracting frames from videos and automatically
stacks images, adjusts contrast, sharpness, etc, along with Seestar S30/50 image stacking.

## Features
- Frame Extraction + Stacking: extracts frames from a video and stacks them into one image.
- (In-Progress) Seestar S30/50 Stacking: stacks images captured by the S30 or S50 telescope.
- (Future) DSLR Stacking: support for DSLR image stacking.

## Requirements
- Python 3.8+
- PySide6 (pip install PySide6) [only if running on IDE]
- OpenCV (pip install opencv-python) [only if running on IDE]
- NumPy (pip install numpy) [only if running on IDE]
- Astroalign (pip install astroalign) [only if running on IDE]

## How to Run Via IDE
1. Clone this repository: 
```
git clone https://github.com/fungjessica/image-processing-app.git
cd image-processing-app
```

2. Install dependencies listed above. 

3. Run the application:
```
python application_scripts/home_window.py
```
