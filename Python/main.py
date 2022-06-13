from mechanism import loadimg, grayscale, translate, rotate, blur, edgedetection

LI = loadimg.loadImg("../Images/vm.png")
IMAGE_1 = LI.getImg()
LI.showImg("LazyPingu Decoded", IMAGE_1, False)

#-------------------------------------------------------------#
# Q1. Convert the image to Grayscale using Image 1 (10 Marks) #
#-------------------------------------------------------------#
GS = grayscale.grayScale("../Images/vm.png", IMAGE_1)
GRAY_IMG = GS.grayImg()
LI.showImg("GrayScale Image of LazyPingu", GRAY_IMG, True)

#---------------------------------------------------------------------------------------------------------------#
# Q2. Apply operations in sequence using Image 1:                                                               #
# Translate -> Rotate -> Blurr image -> Detect edges (20 Marks)                                                 #
#-----------#---------------------------------------------------------------------------------------------------#
# TRANSLATE #
#-----------#
TS = translate.changeDimensionsImg(50, -50, IMAGE_1, "../Images/vm.png")
TRANSLATE_IMG = TS.translateImg()
LI.showImg("Translated (x = 50, y = -50)", TRANSLATE_IMG, True)
# Rotate #
RS = rotate.rotations(IMAGE_1, 90, "../Images/vm.png")
ROTATE_IMG = RS.rotateImg()
LI.showImg("Rotated LazyPingu", ROTATE_IMG, True)
#------#
# BLUR #
#------#
# - Averaging
BR = blur.imgS(IMAGE_1, "../Images/vm.png")
IMAGE_AVERAGE = BR.imgAverageSmoothing((3, 3))
LI.showImg("Average Blurring of Lazypingy", IMAGE_AVERAGE, True)
# Gaussian
IMAGE_GAUSSIAN = BR.imgGaussianSmoothing((3, 3), 0)
LI.showImg("Gaussian Blurring of Lazypingy", IMAGE_GAUSSIAN, True)
# Median
IMAGE_MEDIAN = BR.imgMedianSmoothing(3)
LI.showImg("Median Blurring of Lazypingy", IMAGE_MEDIAN, True)
# Bilateral
IMAGE_BILATERAL = BR.imgBilateralSmoothing(5, (21, 21))
LI.showImg("Bilateral Blurring of Lazypingy", IMAGE_BILATERAL, True)
# Custom blurring
# - Rectangular Focus Inverse Blur
BR.imgCustSmoothing(1, 2, ((120, 30), (220, 140), (255, 255, 255)))
BR1 = blur.imgS(IMAGE_1, "../Images/vm.png")
# - Circular Focus Inverse Blur
BR1.imgCustSmoothing(2, 1, ((155, 90), 65, (255, 255, 255)))
#--------------#
# DETECT EDGES #
#--------------#
ED = edgedetection.imgT(IMAGE_1, "../Images/vm.png")
ED.imgCan("Canny Detector on LazyPingu")
ED.imgSobLap("Sobel and LapLace Detector on LazyPingu", GRAY_IMG)