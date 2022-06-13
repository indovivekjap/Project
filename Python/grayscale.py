#-----------#
# GRAYSCALE #
#-----------#
import cv2
import numpy as np

class grayScale:
    #------------------------- Constructor -------------------------#
    def __init__(self, Img, Path):
        self._IMG = Img
        self._PATH = Path
        self._LENGTH = len(self._PATH)
        # print("Check -> Image_({}), Path_({}), Length_({})".format(self._IMG, self._PATH, self._LENGTH))

    #---------------- Converting Image to Gray Scale ----------------#
    def grayImg(self):
        if self._PATH[self._LENGTH - 3:] == "png" or self._PATH[self._LENGTH - 3:] == "bmp" or self._PATH[self._LENGTH - 3:] == "jpg" or self._PATH[self._LENGTH - 4:] == "jpeg":
            self.__GRAY_IMG = cv2.cvtColor(self._IMG, cv2.COLOR_BGR2GRAY)
            return self.__GRAY_IMG
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("grayImg() stopped!!!", end = "\n----------------------\n")
            return np.zeros((300, 300, 3), dtype = "uint8")