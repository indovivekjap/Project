import cv2
import numpy as np
import mediapipe as mp

class bgRemove2:
    def __init__(self, Img, Path):
        self._IMG = Img
        self._PATH = Path
        self._LENGTH = len(self._PATH)
        self.__HEIGHT, self.__WIDTH, self.__CHANNEL = self._IMG.shape
        # print("Check -> Image_({}), Path_({}), Length_({})".format(self._IMG, self._PATH, self._LENGTH))

    def removeBG2(self):
        if self._PATH[self._LENGTH - 3:] == "png" or self._PATH[self._LENGTH - 3:] == "bmp" or self._PATH[self._LENGTH - 3:] == "jpg" or self._PATH[self._LENGTH - 4:] == "jpeg":
            
            # initialize mediapipe
            self.__MP_SELFIE_SEGMENTATION = mp.solutions.selfie_segmentation
            self.__SELFIE_SEGMENTATION = self.__MP_SELFIE_SEGMENTATION.SelfieSegmentation(model_selection = 1)
            self.__RGB = cv2.cvtColor(self._IMG, cv2.COLOR_BGR2RGB)

            # get the result
            self.__RESULTS = self.__SELFIE_SEGMENTATION.process(self.__RGB)

            # Background masking
            self.__BG_IMG = (249, 245, 240)

            # it returns true or false where the condition applies in the mask
            self.__CONDTION = np.stack((self.__RESULTS.segmentation_mask,) * 3, axis = -1) > 0.5

            # combine frame and background image using the condition
            return np.where(self.__CONDTION, self._IMG, self.__BG_IMG)    
        else:
            print("Image extension not supported!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("removeBG() stopped!!!", end = "\n----------------------\n")