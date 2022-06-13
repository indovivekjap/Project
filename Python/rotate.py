import cv2
import numpy as np

#--------#
# ROTATE #
#--------#
class rotations:
    def __init__(self, Img, Deg, Path):
        self.__SCALE, self._IMG, self._DEG = 1.0, Img, Deg
        self._PATH = Path
        self.__LENGTH = len(self._PATH)
    
    #------------------------- Rotations -------------------------#
    def rotateImg(self):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg":
            (self.__H, self.__W) = self._IMG.shape[:2]
            self.__CENTER = (self.__W//2, self.__H//2)
            self.__MOVEMENT = cv2.getRotationMatrix2D(self.__CENTER, self._DEG, self.__SCALE)
            self.__ROTATE = cv2.warpAffine(self._IMG, self.__MOVEMENT, (self.__W, self.__H))
            return self.__ROTATE
        else: 
            print("Image extension not supported!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("rotateImg() stopped!!!", end = "\n----------------------\n")