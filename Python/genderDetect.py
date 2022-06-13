# Import Libraries
import cv2
import numpy as np

class genderDet:

    # Constructor
    def __init__(self, Image, Path):
        # The gender model architecture
        # https://drive.google.com/open?id=1W_moLzMlGiELyPxWiYQJ9KFaXroQ_NFQ
        self.__GENDER_MODEL = 'gender/deploy_gender.prototxt'
        # The gender model pre-trained weights
        # https://drive.google.com/open?id=1AW3WduLk1haTVAxHOkVS_BEzel1WXQHP
        self.__GENDER_PROTO = 'gender/gender_net.caffemodel'
        # Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
        # substraction to eliminate the effect of illunination changes
        self.__MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        # Represent the gender classes
        self.__GENDER_LIST = ['Male', 'Female']
        # https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
        self.__FACE_PROTO = "gender/deploy.prototxt.txt"
        # https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
        self.__FACE_MODEL = "gender/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        # load face Caffe model
        self.__FACE_NET = cv2.dnn.readNetFromCaffe(self.__FACE_PROTO, self.__FACE_MODEL)
        # Load gender prediction model
        self.__GENDER_NET = cv2.dnn.readNetFromCaffe(self.__GENDER_MODEL, self.__GENDER_PROTO)

    # Returns Faces
    def get_faces(self, frame, confidence_threshold = 0.5):
        self.__FRAME, self.__CONFIDENCE_THRESHOLD = frame, confidence_threshold
        # convert the frame into a blob to be ready for NN input
        self.__BLOB = cv2.dnn.blobFromImage(self.__FRAME, 1.0, (300, 300), (104, 177.0, 123.0))
        # set the image as input to the NN
        self.__FACE_NET.setInput(self.__BLOB)
        # perform inference and get predictions
        __OUTPUT = np.squeeze(self.__FACE_NET.forward())
        # initialize the result list
        __FACES = []
        # Loop over the faces detected
        for i in range(__OUTPUT.shape[0]):
            __CONFIDENCE = __OUTPUT[i, 2]
            if __CONFIDENCE > self.__CONFIDENCE_THRESHOLD:
                __BOX = __OUTPUT[i, 3:7] * np.array([self.__FRAME.shape[1], self.__FRAME.shape[0], self.__FRAME.shape[1], self.__FRAME.shape[0]])
                # convert to integers
                __START_X, __START_Y, __END_X, __END_Y = __BOX.astype(np.int)
                # widen the box a little
                __START_X, __START_Y, __END_X, __END_Y = __START_X - 10, __START_Y - 10, __END_X + 10, __END_Y + 10
                __START_X = 0 if __START_X < 0 else __START_X
                __START_Y = 0 if __START_Y < 0 else __START_Y
                __END_X = 0 if __END_X < 0 else __END_X
                __END_Y = 0 if __END_Y < 0 else __END_Y
                # append to our list
                __FACES.append((__START_X, __START_Y, __END_X, __END_Y))
        return __FACES

    def get_optimal_font_scale(self, text, width):
        self.__TEXT, self.__WIDTH = text, width
        #Determine the optimal font scale based on the hosting frame width
        for __SCALE in reversed(range(0, 60, 1)):
            __TEXT_SIZE = cv2.getTextSize(self.__TEXT, fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = __SCALE/10, thickness = 1)
            __NEW_WIDTH = __TEXT_SIZE[0][0]
            if (__NEW_WIDTH <= self.__WIDTH):
                return __SCALE/10
        return 1

    # from: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        self.__IMAGE, self.__WIDTH, self.__HEIGHT, self.__INTER = image, width, height, inter
        # initialize the dimensions of the image to be resized and
        # grab the image size
        __DIM = None
        (__H, __W) = self.__IMAGE.shape[:2]
        # if both the width and height are None, then return the
        # original image
        if self.__WIDTH is None and self.__HEIGHT is None:
            return self.__IMAGE
        # check to see if the width is None
        if self.__WIDTH is None:
            # calculate the ratio of the height and construct the
            # dimensions
            __R = self.__HEIGHT / float(__H)
            __DIM = (int(__W * __R), self.__HEIGHT)
        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            __r = self.__WIDTH / float(__W)
            __DIM = (self.__WIDTH, int(__H * __R))
        # resize the image
        return cv2.resize(self.__IMAGE, __DIM, interpolation = self.__INTER)
    
    #Predict the gender of the faces showing in the image
    def predict_gender(self, input_path: str, ch):
        # Read Input Image
        img = cv2.imread(input_path)
        # resize the image, uncomment if you want to resize the image
        # img = cv2.resize(img, (frame_width, frame_height))
        # Take a copy of the initial image and resize it
        frame = img.copy()
        frame_width, frame_height = frame.shape[0], frame.shape[1]
        if frame.shape[1] > frame_width:
            frame = self.image_resize(frame, width=frame_width, )
        # predict the faces
        faces = self.get_faces(frame)
        # Loop over the faces detected
        # for idx, face in enumerate(faces):
        for i, (start_x, start_y, end_x, end_y) in enumerate(faces):
            face_img = frame[start_y: end_y, start_x: end_x]
            # image --> Input image to preprocess before passing it through our dnn for classification.
            # scale factor = After performing mean substraction we can optionally scale the image by some factor. (if 1 -> no scaling)
            # size = The spatial size that the CNN expects. Options are = (224*224, 227*227 or 299*299)
            # mean = mean substraction values to be substracted from every channel of the image.
            # swapRB=OpenCV assumes images in BGR whereas the mean is supplied in RGB. To resolve this we set swapRB to True.
            blob = cv2.dnn.blobFromImage(image=face_img, scalefactor=1.0, size=(
                227, 227), mean = self.__MODEL_MEAN_VALUES, swapRB = False, crop = False)
            # Predict Gender
            self.__GENDER_NET.setInput(blob)
            gender_preds = self.__GENDER_NET.forward()
            i = gender_preds[0].argmax()
            gender = self.__GENDER_LIST[i]
            gender_confidence_score = gender_preds[0][i]
            # Draw the box
            label = "{}-{:.2f}%".format(gender, gender_confidence_score*100)
            yPos = start_y - 15
            while yPos < 15:
                yPos += 15
            # get the font scale for this image size
            optimal_font_scale = self.get_optimal_font_scale(label,((end_x-start_x)+25))
            box_color = (255, 0, 0) if gender == "Male" else (147, 20, 255)
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)
            # # Label processed image
            # Value = cv2.putText(frame, label, (start_x, yPos),
            #             cv2.FONT_HERSHEY_SIMPLEX, optimal_font_scale, box_color, 2)
        if ch == "frame":
            return frame
        if ch == "label":
            return label