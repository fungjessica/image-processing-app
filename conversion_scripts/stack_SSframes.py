import os
import cv2
import numpy as np
from glob import glob

# Run second 

# Align frames using ORB feature matching
def align_images(base_img, img):
    """Align img to base_img using ORB feature matching."""
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(base_img, None)
    kp2, des2 = orb.detectAndCompute(img, None)

    # Match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    if len(matches) < 10:
        return None  # Not enough matches

    # Find homography
    src_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    return cv2.warpPerspective(img, M, (base_img.shape[1], base_img.shape[0]))

# Stack frames using feature-based alignment
def stack_frames(image_folder, output_file):
    files = sorted(glob(os.path.join(image_folder, "*.jpg")))  # Change to .png if needed
    if len(files) == 0:
        print("No images found!")
        return
    
    print(f"Processing {len(files)} frames...")

    # Use first frame as reference
    base_img = cv2.imread(files[0], cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    stacked_image = np.zeros_like(base_img)
    count = 0

    for file in files:
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
        aligned = align_images(base_img, img)

        if aligned is not None:
            stacked_image += aligned
            count += 1

    if count > 0:
        stacked_image /= count  # Average stack
        stacked_image = (stacked_image * 255).astype(np.uint8)
        cv2.imwrite(output_file, stacked_image)
        print(f"Stacked image saved as {output_file}")
    else:
        print("No images aligned successfully!")

# Run stacking
image_folder = "seestar_frames"  
output_folder = "stacked_SSimages"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "stacked_SSseestar.png")
stack_frames(image_folder, output_file)