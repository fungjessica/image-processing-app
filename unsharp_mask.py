import cv2
import os

# run fourth 

# apply unsharpening on image
# https://en.wikipedia.org/wiki/Unsharp_masking 
def unsharp_mask(image, sigma=1.0, amount=1.5, threshold=0):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    return sharpened

# load files and call functions
image_path = "stacked_images/stacked_jupiter.png"  
image = cv2.imread(image_path)

if image is None:
    print(f"error: Could not load {image_path}")
else:
    sharpened = unsharp_mask(image, sigma=1.0, amount=2.0)
    
    # conver to CIELAB color space
    # https://en.wikipedia.org/wiki/CIELAB_color_space
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    
    # save to file
    output_path = "stacked_images/sharpened_jupiter.png" #change for other planets
    cv2.imwrite(output_path, sharpened)
    print(f"saved sharpened image as {output_path}")