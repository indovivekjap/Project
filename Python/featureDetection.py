import cv2

class FaceDetector:
    def __init__(self, Img, Path):
        self.__BLOCK = False
        self._IMG = Img
        self._PATH = Path
        self.__LENGTH = len(self._PATH)
        self.face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Note the change

    def imgDetect(self):
        if self._PATH[self.__LENGTH - 3:] == "png" or self._PATH[self.__LENGTH - 3:] == "bmp" or self._PATH[self.__LENGTH - 3:] == "jpg" or self._PATH[self.__LENGTH - 4:] == "jpeg":
            rects = self.face_cascade.detectMultiScale(self._IMG, scaleFactor = 1.3, minNeighbors = 5, minSize = (30,30), flags = cv2.CASCADE_SCALE_IMAGE)
            return rects
        else:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("detect() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True