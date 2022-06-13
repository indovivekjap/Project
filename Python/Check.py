from mechanism import loadimg, grayscale, translate, rotate, blur, edgedetection

LI = loadimg.loadImg("../Images/coins.png")
IMAGE_1 = LI.getImg()
LI.showImg("LazyPingu Decoded", IMAGE_1, False)

#-------------------------------------------------------------#
# Q1. Convert the image to Grayscale using Image 1 (10 Marks) #
#-------------------------------------------------------------#
GS = grayscale.grayScale("../Images/coins.png", IMAGE_1)
GRAY_IMG = GS.grayImg()
LI.showImg("GrayScale Image of LazyPingu", GRAY_IMG, True)