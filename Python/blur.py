import cv2
import numpy as np

#------#
# BLUR #
#------#
class imgS:
    def __init__(self, Img, Path):
        self.__BLOCK = False
        self._IMG = Img
        self._PATH = Path
        self.__LENGTH = len(self._PATH)

    def __smoothingTech(self, ChAlgo):
        self.__CHOICE_ALGORITHM = ChAlgo
        self.__RESULT = None
        if self.__CHOICE_ALGORITHM == 1:
            self.__RESULT = self.imgAverageSmoothing((21, 21))
        elif self.__CHOICE_ALGORITHM == 2:
            self.__RESULT = self.imgGaussianSmoothing((21, 21), 0)
        elif self.__CHOICE_ALGORITHM == 3:
            self.__RESULT = self.imgMedianSmoothing(21)
        elif self.__CHOICE_ALGORITHM == 4:
            self.__RESULT = self.imgBilateralSmoothing(5, (21, 21))
        return self.__RESULT

    def imgAverageSmoothing(self, Kernel):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            (self._KERNEL_X, self._KERNEL_Y) = Kernel
            self.__BLURRED = cv2.blur(self._IMG, (self._KERNEL_X, self._KERNEL_Y))
            return self.__BLURRED
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgAverageSmoothing() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    # Setting 3rd variable as 0 in GaussianBlur(, , 0) 
    # - Asking method to compute according to kernel size
    def imgGaussianSmoothing(self, Kernel, GaussianValue):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            (self._KERNEL_X, self._KERNEL_Y) = Kernel
            self._GAUSSIAN_VALUE = GaussianValue
            self.__GAUSSIAN = cv2.GaussianBlur(self._IMG, (self._KERNEL_X, self._KERNEL_Y), self._GAUSSIAN_VALUE)
            return self.__GAUSSIAN
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgGaussianSmoothing() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    def imgMedianSmoothing(self, MedianValue):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            self._MEDIAN_VALUE = MedianValue
            self.__MEDIAN = cv2.medianBlur(self._IMG, self._MEDIAN_VALUE)
            return self.__MEDIAN
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgMedianSmoothing() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    def imgBilateralSmoothing(self, ColorVal, SizeVal):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            self._COLOR_VAL, (self._X, self._Y) = ColorVal, SizeVal
            self.__BILATERAL = cv2.bilateralFilter(self._IMG, self._COLOR_VAL, self._X, self._Y)
            return self.__BILATERAL
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgBilateralSmoothing() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    def imgCustSmoothing(self, ChShapeMask, ChAlgorithm, ShapeDetails):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            self._CHOICE_SHAPE_MASK, self._CHOICE_ALGORITHM = ChShapeMask, ChAlgorithm
            (self._START, self._END, self._COLOR) = ShapeDetails
            if self._CHOICE_SHAPE_MASK == 1:
                self.__BLURR_IMG = self.__smoothingTech(self._CHOICE_ALGORITHM)
                self.__MASK = np.zeros(self._IMG.shape, dtype = "uint8")
                self.__MASK = cv2.rectangle(self.__MASK, self._START, self._END, color = self._COLOR, thickness = -1)
                self.__CUST_BLURR_IMAGE = np.where(self.__MASK == (255, 255, 255), self._IMG, self.__BLURR_IMG)
                self.imgSDisp(self.__CUST_BLURR_IMAGE, "Rectangle Blurr Focus")
            elif self._CHOICE_SHAPE_MASK == 2:
                self.__BLURR_IMG = self.__smoothingTech(self._CHOICE_ALGORITHM)
                self.__MASK = np.zeros(self._IMG.shape, dtype = "uint8")
                self.__MASK = cv2.circle(self.__MASK, self._START, self._END, color = self._COLOR, thickness = -1)
                self.__CUST_BLURR_IMAGE = np.where(self.__MASK == (255, 255, 255), self._IMG, self.__BLURR_IMG)
                self.imgSDisp(self.__CUST_BLURR_IMAGE, "Circle Blurr Focus")
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgCustSmoothing() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    def imgSDisp(self, Img, WinName):
        if self.__BLOCK:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgSDisp() stopped!!!", end = "\n----------------------\n")
        else:
            self._IMG, self._WIN_NAME = Img, WinName
            cv2.imshow(self._WIN_NAME, self._IMG)
            print("{} displayed successfully".format(self._WIN_NAME), end = "\n----------------------\n")
            cv2.waitKey(0)
            cv2.destroyWindow(self._WIN_NAME)