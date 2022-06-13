import cv2
import numpy as np

#-----------------#
# TRANSFORMATIONS #
#-----------------#
class changeDimensionsImg:
    def __init__(self, X, Y, Img, Path):
        self._PATH = Path
        self._X, self._Y, self._IMG = X, Y, Img
        self.__LENGTH = len(self._PATH)

    #------------------------- Displacement/Translation -------------------------#
    def translateImg(self):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg":
            self.__MOVEMENT = np.float32([[1, 0, self._X], [0, 1, self._Y]])
            # print("Image Shape (Height, Width, Channels) ->", self._IMG.shape)
            self.__TRANSLATE = cv2.warpAffine(self._IMG, self.__MOVEMENT, (self._IMG.shape[0], self._IMG.shape[1]))
            return self.__TRANSLATE
        else: 
            print("Image extension not supported!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("translateImg() stopped!!!", end = "\n----------------------\n")