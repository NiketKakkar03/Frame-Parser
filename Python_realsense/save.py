import pyrealsense2 as rs
import numpy as np
import cv2
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Create MP4 video writer with MP4V codec
color_writer = cv2.VideoWriter('color3.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480), True)

pipeline.start(config)

# Set timer for 30 seconds
start_time = time.time()
duration = 90  # seconds

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        if not color_frame:
            continue
        
        color_image = np.asanyarray(color_frame.get_data())
        color_writer.write(color_image)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Print remaining time
        remaining_time = duration - elapsed_time
        print(f"Recording... {remaining_time:.1f}s remaining")
        
        # Stop recording after 30 seconds
        if elapsed_time >= duration:
            print("30 seconds elapsed. Stopping recording...")
            break
        
        if cv2.waitKey(1) == ord('q'):
            print("Recording stopped by user.")
            break
finally:
    color_writer.release()
    pipeline.stop()
    print("Recording complete. File saved as color.mp4")
