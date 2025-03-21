# run first 

import cv2 
import os

def extract_frames(video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    return output_folder  

# old code from geeks for geeks 
# https://www.geeksforgeeks.org/python-program-extract-frames-using-opencv/

'''
# Function to extract frames 
def FrameCapture(path): 
  
    # Path to video file 
    vidObj = cv2.VideoCapture(path) 
    frames = "moon_frames"
    os.makedirs(frames, exist_ok=True)
    # Used as counter variable 
    count = 0
  
    # checks whether frames were extracted 
    success = 1
  
    while success: 
  
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
  
        # Saves the frames with frame-count 
        cv2.imwrite(os.path.join(frames, "frame%d.jpg" % count), image) 
  
        count += 1
  
  
# Driver Code 
if __name__ == '__main__': 
    video_path = os.path.join("videos", "ssMoon7-19.mp4") #change for different videos
    # Calling the function 
    FrameCapture(video_path) '
'''