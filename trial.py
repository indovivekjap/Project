from cProfile import label
from Python.loadimg import loadImg
from Python.grayscale import grayScale
from Python.featureDetection import FaceDetector
from Python.genderDetect import genderDet

import cv2

PATH = "Project_extra/Sid-Roy.jpg"

# Setting image
LI = loadImg(PATH)
IMG = LI.getImg()
# LI.showImg("Sid",  LI.getImg(), 1)

# GrayScale
GS = grayScale(IMG, PATH)
Gray = GS.grayImg()

# Face Detection
FDR = FaceDetector(Gray, PATH)
rect = FDR.imgDetect()
for (x, y, w, h) in rect:
    rect = cv2.rectangle(IMG, (x, y), (x + w, y + h), (0, 255, 0), 2)
LI.showImg("wow", rect, 1)

# Gender detection
GDTC = genderDet(IMG, PATH)
GENDER_IMAGE = GDTC.predict_gender(PATH, "frame")
WinName = GDTC.predict_gender(PATH, "label")
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (50, 50)
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 0, 255)
# Line thickness of 2 px
thickness = 2
# Using cv2.putText() method
gender, confidence = WinName.split("-")
print(gender, confidence)
image = cv2.putText(GENDER_IMAGE, WinName, org = org, color = color, fontFace = 2, fontScale = 1)
LI.showImg(WinName, image, 0)