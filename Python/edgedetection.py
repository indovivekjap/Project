import cv2
import numpy as np

#---------------------------------#
# Detection - Edges and Gradients #
#---------------------------------#
class imgT:
    def __init__(self, Img, Path):
        self.__BLOCK = False
        self._IMG = Img
        self._PATH = Path
        self.__LENGTH = len(self._PATH)

    def imgSobLap(self, WinName, GrayImg):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            self._WIN_NAME = WinName
            self._GRAY_IMG = GrayImg
            # self.__GRAY = cv2.cvtColor(self._IMG, cv2.COLOR_BGR2GRAY)
            self.__LAP = cv2.Laplacian(self._GRAY_IMG, cv2.CV_64F)
            self.__LAP = np.uint8(np.absolute(self.__LAP))
            # self.imgDDisp(self._WIN_NAME, self.__LAP)
            # Sobel and Gradient Detction logic
            self.__SOBEL_X = cv2.Sobel(self._GRAY_IMG, cv2.CV_64F, 1, 0)
            self.__SOBEL_Y = cv2.Sobel(self._GRAY_IMG, cv2.CV_64F, 0, 1)
            self.__SOBEL_X = np.uint8(np.absolute(self.__SOBEL_X))
            self.__SOBEL_Y = np.uint8(np.absolute(self.__SOBEL_Y))
            self.__SOBEL_COMBINED = cv2.bitwise_or(self.__SOBEL_X, self.__SOBEL_Y)
            # self.imgDDisp("Sobel X", self.__SOBEL_X)
            # self.imgDDisp("Sobel Y", self.__SOBEL_Y)
            # self.imgDDisp("Sobel Combined", self.__SOBEL_COMBINED)
            return self.__SOBEL_COMBINED
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgSobLap() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    def imgCan(self, WinName):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg": 
            self._WIN_NAME = WinName
            self.__GRAY = cv2.cvtColor(self._IMG, cv2.COLOR_BGR2GRAY)
            self.__BLURR = cv2.GaussianBlur(self.__GRAY, (5, 5), 0)
            # self.imgDDisp("Blurred", self.__BLURR)
            # Canny Detector
            return cv2.Canny(self.__BLURR, 30, 150)
            # self.imgDDisp("Canny", self.__CANNY)
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgCan() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True
    
    def imgDDisp(self, WinName, Img):
        if self.__BLOCK:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgDDisp() stopped!!!", end = "\n----------------------\n")
        else:
            self._IMG, self._WIN_NAME = Img, WinName
            cv2.imshow(self._WIN_NAME, self._IMG)
            print("{} displayed successfully".format(self._WIN_NAME), end = "\n----------------------\n")
            cv2.waitKey(0)
            cv2.destroyWindow(self._WIN_NAME)