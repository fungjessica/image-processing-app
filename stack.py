import os
import cv2
import numpy as np
from glob import glob

# run second 

# find the center of a frame
def find_center(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # apply threshold to isolate planet
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    
    # find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None  

    # find largest contour in frame
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)

    if M["m00"] == 0:
        return None  

    # find contour center
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    return (cx, cy)

# shift frames
def shift_image(image, shift_x, shift_y):
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    shifted_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted_image

# stack frames
def stack_frames(image_folder, output_file):
    files = sorted(glob(os.path.join(image_folder, "*.jpg")))  
    if len(files) == 0:
        print("No images found!")
        return
    
    print(f"Processing {len(files)} frames...")

    # use first frame as reference to be stacked
    base_img = cv2.imread(files[0])
    base_center = find_center(base_img)
    
    if base_center is None:
        print("Error: Couldn't detect planet in the first frame!")
        return
    
    stacked_image = np.float32(base_img) / 255  
    
    for file in files[1:]:
        img = cv2.imread(file)
        center = find_center(img)

        if center is None:
            print(f"Skipping {file}")
            continue

        shift_x = base_center[0] - center[0]
        shift_y = base_center[1] - center[1]
        
        # align image
        aligned_img = shift_image(img, shift_x, shift_y)
        stacked_image += np.float32(aligned_img) / 255

    # find average stack
    stacked_image /= len(files)
    stacked_image = (stacked_image * 255).astype(np.uint8)

    # save image
    cv2.imwrite(output_path, stacked_image)
    print(f"Saved stacked image to {output_file}")

image_folder = "frames"  
output_folder = "stacked_images"
os.makedirs(output_folder, exist_ok=True)
output_file = "stacked_jupiter.png" #change for other planets
output_path = os.path.join(output_folder, output_file)
stack_frames(image_folder, output_file)