import cv2
import numpy as np

class bgRemove:
    def __init__(self, Img, Path):
        self._IMG = Img
        self._PATH = Path
        self._LENGTH = len(self._PATH)
        # print("Check -> Image_({}), Path_({}), Length_({})".format(self._IMG, self._PATH, self._LENGTH))

    def removeBG(self):
        if self._PATH[self._LENGTH - 3:] == "png" or self._PATH[self._LENGTH - 3:] == "bmp" or self._PATH[self._LENGTH - 3:] == "jpg" or self._PATH[self._LENGTH - 4:] == "jpeg":
            self.__GRAY_IMG = cv2.cvtColor(self._IMG, cv2.COLOR_BGR2GRAY)
            # Find the threshold
            _, self.__THRESH = cv2.threshold(self.__GRAY_IMG, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            # Find the image contours
            self.__IMG_CONTOURS = cv2.findContours(self.__THRESH, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
            # Sort the contours
            self.__IMG_CONTOURS = sorted(self.__IMG_CONTOURS, key = cv2.contourArea)
            for i in self.__IMG_CONTOURS:
                if cv2.contourArea(i) > 1000000:
                    break
            # Generate the mask using np.zeros
            self.__MASK = np.zeros(self._IMG.shape[:2], np.uint8)
            # Draw contours
            cv2.drawContours(self.__MASK, [i],-1, 255, -1)
            # Apply the bitwise_and operator
            self.__BG_REMOVE_IMG = cv2.bitwise_and(self._IMG, self._IMG, mask = self.__MASK)
            return self.__BG_REMOVE_IMG
        else:
            print("Image extension not supported!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("removeBG() stopped!!!", end = "\n----------------------\n")