import cv2
import os

# run fifth 

# adjust image histogram (constrast) via CLAHE
# https://www.geeksforgeeks.org/clahe-histogram-eqalization-opencv/
def enhance_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)

    enhanced = cv2.merge((l, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

# find and appy to images
image_path = "stacked_images/sharpened_jupiter.png" #change for other planets
image = cv2.imread(image_path)

output_path = "stacked_images/constrast_jupiter.png" #change for other planets

enhanced = enhance_contrast(image)
cv2.imwrite(output_path, enhanced)
print(f"saved enhanced image as {output_path}")