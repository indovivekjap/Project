#----------------#
# Loading Images #
#----------------#
import cv2

class loadImg:
    #------------------------- Constructor -------------------------#
    def __init__(self, Path):
        self.__BLOCK = False
        self._PATH = Path
        self._LENGTH = len(self._PATH)

    #------------------------- Loading Image -------------------------#
    def getImg(self):
        if self._PATH[self._LENGTH - 3:] == "png" or self._PATH[self._LENGTH - 3:] == "bmp" or self._PATH[self._LENGTH - 3:] == "jpg" or self._PATH[self._LENGTH - 4:] == "jpeg":
            self._IMG = cv2.imread(self._PATH)
            print("Image returned!", end = "\n----------------------\n")
            return self._IMG
        else: 
            print("Image extension not supported!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("getImg() stopped!!!", end = "\n----------------------\n")
            self.__BLOCK = True

    #------------------------- Saving Image -------------------------#
    def imgSave(self, Img, FileName, Path):
        if self.__BLOCK:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("imgSave() stopped!!!", end = "\n----------------------\n")
        else:
            self._IMG = Img
            self._FILE_NAME = FileName
            self._PATH = Path
            cv2.imwrite((self._PATH + self._FILE_NAME), self._IMG)
            print("Image Saved!!!", end = "\n----------------------\n")

    #------------------------- Displaying Loaded Image -------------------------#
    def showImg(self, WinName, Img, Ch):
        if self.__BLOCK:
            print("Cannot run for unsupported file types!!!\n please provide file with \".bmp, .jpg, .jpeg or .png\" extension")
            print("showImg() stopped!!!", end = "\n----------------------\n")
        else:
            self._WINNAME = WinName
            self._CHOICE = Ch
            if self._CHOICE:
                self.__IMG = Img
                cv2.imshow(self._WINNAME, self.__IMG)
            else:
                cv2.imshow(self._WINNAME, self._IMG)
            print("Image Displayed!!")
            cv2.waitKey(0)
            cv2.destroyWindow(self._WINNAME)
            print("Displayed Image Window Closed!!", end = "\n----------------------\n")