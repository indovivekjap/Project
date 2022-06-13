    # DataFlair background removal
# import necessary packages
import os
import cv2
import numpy as np
import mediapipe as mp

img = cv2.imread("f1_75.jpg")

# initialize mediapipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection = 1)

height, width, channel = img.shape

RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# get the result
results = selfie_segmentation.process(RGB)

# extract segmented mask
mask = results.segmentation_mask
# show outputs
cv2.imshow("mask", mask)
cv2.imshow("Image", img)

bgImg = np.zeros((height, width, channel), np.uint8)

# it returns true or false where the condition applies in the mask
condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

# combine frame and background image using the condition
output_image = np.where(condition, img, bgImg)
cv2.imshow("Final", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()