# Recording Video with Intel RealSense Camera

Follow these steps to capture video data using the RealSense camera for object detection and tracking.

## Prerequisites
- RealSense camera disconnected from rover
- USB-C cable available
- Access to QSET room tools

## Setup Instructions

### 1. Disconnect from Rover
Disconnect the RealSense camera from the rover's mini PC using the appropriate tool located in the QSET room.

### 2. Connect to Laptop
Connect the camera to your laptop using the USB-C cable (the same cable used to connect to the rover's mini PC).

### 3. Verify Camera Connection
Run the main script to confirm the camera feed is working:

You should see the camera output displayed on your screen.

## Recording Process

### 4. Configure Output File
Before recording, update the output filename in `save.py`:
- Use the naming convention: `color.mp4`, `color1.mp4`, `color2.mp4`, etc.
- Increment the number for each new recording session

### 5. Position and Record
- Position the target object in front of the RealSense camera
- Ensure proper lighting and distance
- Run the recording script
