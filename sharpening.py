import cv2
import numpy as np
import os

# run third 

# perform wavelet sharpen similar to Registax
# https://www.astronomie.be/registax/linkedwavelets.html
def wavelet_sharpen(image, levels=5, strength=1.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255

    # gaussian decomposition
    gp = [gray]
    for i in range(levels):
        gray = cv2.pyrDown(gray)
        gp.append(gray)

    # upsample frames
    lp = [gp[levels]]
    for i in range(levels, 0, -1):
        upsampled = cv2.pyrUp(lp[-1])

        # resize frames
        upsampled = cv2.resize(upsampled, (gp[i-1].shape[1], gp[i-1].shape[0]))

        laplacian = cv2.subtract(gp[i-1], upsampled)
        lp.append(laplacian * strength)

    # layers match in size
    for i in range(1, len(lp)):
        lp[i] = cv2.resize(lp[i], (gp[0].shape[1], gp[0].shape[0]))

    # reconstruct image
    sharpened = gp[0] + sum(lp[1:])  
    sharpened = np.clip(sharpened * 255, 0, 255).astype(np.uint8)

    return cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)

# load image
image_path = os.path.join("stacked_images", "stacked_jupiter.png") #change for other planets
image = cv2.imread(image_path)

if image is None:
    print(f"error: Could not load {image_path}")
else:
    sharpened = wavelet_sharpen(image, levels=5, strength=0.1)
    output_path = os.path.join("stacked_images", "sharpened_jupiter.png") #change for other planets
    cv2.imwrite(output_path, sharpened)
    print(f"saved sharpened image as {output_path}")