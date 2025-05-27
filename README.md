# eTapon: An IoT-based Smart Trash Bin Utilizing Machine Learning for School Waste Segregation

**eTapon** is a project development research paper from the **Diploma in Computer Engineering Technology 3-1**, **Polytechnic University of the Philippines – Institute of Technology**, developed by:

- Gladwin Ferdz I. Del Rosario  
- Xander Alfaro  
- Jhedi Castro  
- Baron Bueno  
- James Lester Colle  

**eTapon** is an IoT-based smart trash bin that leverages **YOLOv11s**, trained on a custom dataset, to accurately detect and classify waste as either **biodegradable** or **non-biodegradable**.

---

# Code Documentation

## Project Setup

The eTapon codebase uses a modular folder structure. Its main folders are:
- root: contains the base files of the project
- Arduino: the code for the Arduino to control the servo motors
- camera: picamera initializer of the raspberry pi
- categories: the list of biodegradable and non-biodegradable items for categorization.
- services: business logic of the program/project.

## main.py

the main.py file is the entry point of the program an loads the GUI launcher for the real-time object detection system using Tkinter, a camera module (picamera2), and custom services for frame processing of the machine learning model of eTapon.

### main.py file imports
```python
# Insert main logic or sample code from main.py here
# Example:
import tkinter as tk
from tkinter import ttk
from camera.webcam import get_camera, read_frame
from services.detection_service import process_frame
from picamera2 import Picamera2
from PIL import Image, ImageTk
```
This block imports necessary modules and libraries for the application.
- tkinter and ttk provide tools for building the GUI.
- get_camera and read_frame from camera.webcam handle camera initialization and frame retrieval.
- process_frame from services.detection_service applies trash detection logic on each frame.
- Picamera2 is used to interface with the Raspberry Pi Camera.
- Image and ImageTk from PIL are used to convert and display camera frames on the GUI canvas.

### CameraApp Class Initialization and GUI Layout
The main class in the script is CameraApp, which encapsulates the entire logic for creating and running the camera application.
```python
class CameraApp:
    def __init__(self, window, window_title):
        ...
```
This block defines the CameraApp class, which encapsulates all functionalities and UI components of the application. The constructor method __init__ initializes the main window, configures the layout, and sets up UI widgets like the video canvas, detection toggle button, counters, and log box. It also sets up initial variables for the counters and flags. The layout is organized using nested frames for better structure and responsiveness.

### Canvas Setup for Displaying Video Frames
```python
self.canvas = tk.Canvas(left_frame, width=640, height=480, bg="black")
self.canvas.pack()
```

### Toggle Detection Button
```python
self.toggle_button = ttk.Button(
    left_frame,
    text="Start Detection",
    command=self.toggle_detection
)
self.toggle_button.pack(pady=10)
```
A button is added below the video canvas that allows users to start or stop the detection process. It calls the toggle_detection method when clicked, dynamically changing its label based on the current detection state.