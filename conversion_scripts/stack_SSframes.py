import os
import cv2
import numpy as np
import sep
from glob import glob
from astropy.io import fits
import astroalign

# function to adjust image contrast
def contrast_stretch(image, low_pct=0.5, high_pct=99.9):
    low = np.percentile(image, low_pct)
    high = np.percentile(image, high_pct)
    print(f"Stretching from {low:.2f} to {high:.2f}")
    stretched = np.clip((image - low) / (high - low), 0, 1)
    return (stretched * 255).astype(np.uint8)

# function to detect stars and return their centroids
def detect_stars(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    data = gray.astype(np.float32) 
    bkg = sep.Background(data)
    data_sub = data - bkg  
    stars = sep.extract(data_sub, 5.0, err=bkg.globalrms)  
    return np.column_stack((stars['x'], stars['y']))  

# function to align images based on star positions
def align_images(base_img, img):
    try:
        aligned, _ = astroalign.register(img, base_img)
        return aligned
    except Exception as e:
        print(f"Alignment failed: {e}")
        return None
    
# function to stack images using median stacking
def stack_images(image_folder, output_file):
    files = sorted(glob(os.path.join(image_folder, "*.jpg")) + glob(os.path.join(image_folder, "*.png")) + glob(os.path.join(image_folder, "*.tif")))
    if not files:
        print("No images found!")
        return

    print(f"Processing {len(files)} images...")

    base_img = cv2.imread(files[0], cv2.IMREAD_COLOR)
    if base_img is None:
        print("Failed to load base image.")
        return

    aligned_images = []

    for file in files:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        if img is None:
            continue

        aligned = align_images(base_img, img)
        if aligned is not None:
            aligned_images.append(aligned)
            print(f"Successfully aligned: {file}")
        else:
            print(f"Skipping file {file} due to failed alignment.")

    if not aligned_images:
        print("No images aligned successfully!")
        return

    print(f"Stacking {len(aligned_images)} aligned images.")

    # convert list to numpy array. shape: (N, H, W, 3)
    aligned_array = np.array(aligned_images)  

    # stack each color channel separately (RGB)
    stacked = np.zeros_like(aligned_array[0], dtype=np.float32)
    for c in range(3):  
        channel_median = np.median(aligned_array[:, :, :, c].astype(np.float32), axis=0)
        stacked[:, :, c] = channel_median

    stacked = contrast_stretch(stacked, low_pct=0.5, high_pct=99.9)

    # save the stacked image
    cv2.imwrite(output_file, stacked)
    print(f"Stacked image saved as {output_file}")

image_folder = "/Users/jessicafung/Documents/phys180/seestar_frames/M 33-sub"
output_folder = "stacked_SSimages"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "stacked_m33ss.png")
stack_images(image_folder, output_file)