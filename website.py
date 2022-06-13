# streamlit run website.py

# Installed Libraries
from streamlit_option_menu import option_menu

# Locally created libraries
from Python.loadimg import loadImg
from Python.backgroundremoval import bgRemove
from Python.backgroundremoval2 import bgRemove2
from Python.grayscale import grayScale
from Python.translate import changeDimensionsImg
from Python.rotate import rotations
from Python.blur import imgS
from Python.edgedetection import imgT
from Python.featureDetection import FaceDetector
from Python.genderDetect import genderDet
from streamlit_image_comparison import image_comparison

# Utils
import cv2
import time
import os
import numpy as np
import streamlit as st
timestr = time.strftime("%Y%m%d-%H%M%S")

# Remove .streamlit from page title tag
st.set_page_config(
   page_title = "Vivek Vision",
   page_icon = "🧊",
   layout = "wide",
   initial_sidebar_state = "expanded",
)

# Custom Method to find extension of a file name
def extensionFileName(file_name):
    __EXTENSION = ""
    if file_name[len(file_name) - 3:] == "png" or file_name[len(file_name) - 3:] == "jpg" or file_name[len(file_name) - 3:] == "bmp":
        __EXTENSION += file_name[len(file_name) - 3:]
    elif file_name[len(file_name) - 4:] == "jpeg":
        __EXTENSION += file_name[len(file_name) - 4:]
    return "." + __EXTENSION

# delete image after use
def remove_img(path, img_name):
    os.remove(path + '/' + img_name)
    # check if file exists or not
    if os.path.exists(path + '/' + img_name) is False:
        # file did not exists
        return True
    else: 
        return False

# if Text file is empty
def file_is_empty(path):
    return os.stat(path).st_size==0

# if File exists
def file_exists(path):
    return os.path.exists('readme.txt')

# if images left from previous run
def remove_images(__EXTENSION):
    if file_exists("Images/upload" + __EXTENSION):
        remove_img("Images/", "upload" + __EXTENSION)

    # Remove "Background removed" image
    if file_exists("Images/bgremove" + __EXTENSION): 
        remove_img("Images/", "bgremove" + __EXTENSION)
    
    # Remove "Grayscale" image
    if file_exists("Images/grayscale" + __EXTENSION):
        remove_img("Images/", "grayscale" + __EXTENSION)
    
    # Remove "Translate" image
    if file_exists("Images/translate" + __EXTENSION):
        remove_img("Images/", "translate" + __EXTENSION)

    # Remove "Rotate" image
    if file_exists("Images/rotate" + __EXTENSION):
        remove_img("Images/", "rotate" + __EXTENSION)

    # Remove "Blurr" image
    if file_exists("Images/median" + __EXTENSION):
        remove_img("Images/", "median" + __EXTENSION)

    # Remove "Detected Edge" image
    if file_exists("Images/detect" + __EXTENSION):
        remove_img("Images/", "detect" + __EXTENSION)    

# Method to incorporate multiple operations
def fullMethod(FileNameWithoutExtension, ImageCaption, Operation, SuccessMessage, FinalFileName):
    # Check for Wether image is uploaded or not!
    try:
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file

        # open text file in read mode
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file
            
        # Loading file name from a text file
        __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
        __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
            
        # Load image as an array for OpenCV operations
        LI = loadImg(__FILE_WITH_EXTENSION)
        IMG = LI.getImg()

        if Operation == 1:
            BR = bgRemove2(IMG, __FILE_WITH_EXTENSION)    
            Value = BR.removeBG2()

        if Operation == 2:  
            GS = grayScale(IMG, __FILE_WITH_EXTENSION)
            Value = GS.grayImg()
        
        if Operation == 3:
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                x = st.number_input('How much to be displaced - X Axis', min_value = -(IMG.shape[1]/2), max_value = (IMG.shape[1]/2))
                st.write('The current number is ', x, '(Negative, Postive - Left, Right)')
            with col2:
                y = st.number_input('How much to be displaced - Y Axis', min_value = -(IMG.shape[0]/2), max_value = (IMG.shape[0]/2))
                st.write('The current number is ', y, '(Negative, Postive) - (Down, Up)')
            CDI = changeDimensionsImg(x, y, IMG, __FILE_WITH_EXTENSION)
            Value = CDI.translateImg()
        
        if Operation == 4:
            __direction = st.radio("Select Rotational Direction", ('Clockwise', 'Anti-Clockwise'))
            if __direction == 'Clockwise':
                rot = st.number_input('How much to be rotated', min_value = -359, max_value = 0)
            else:
                rot = st.number_input('How much to be rotated', min_value = 0, max_value = 359)
            RTS = rotations(IMG, rot, __FILE_WITH_EXTENSION)
            Value = RTS.rotateImg()
        
        if Operation == 5:
            BLR = imgS(IMG, __FILE_WITH_EXTENSION)
            __technique = st.radio("Select one Blurring Algorithm", ('Average', 'Gaussian', 'Median', 'Bilateral'))
            if __technique == 'Average':
                Value = BLR.imgAverageSmoothing((21, 21))
            if __technique == 'Gaussian':
                Value = BLR.imgGaussianSmoothing((21, 21), 0)
            if __technique == 'Median':
                Value = BLR.imgMedianSmoothing(21)
            if __technique == 'Bilateral':
                Value = BLR.imgBilateralSmoothing(5, (21, 21))
        
        if Operation == 6:
            DTE = imgT(IMG, __FILE_WITH_EXTENSION)
            __technique = st.radio("Select one Blurring Algorithm", ('Canny', 'Sobel Laplace'))
            if __technique == 'Canny':
                Value = DTE.imgCan("")
            if __technique == 'Sobel Laplace':
                Value = DTE.imgSobLap("", grayScale(IMG, __FILE_WITH_EXTENSION).grayImg())

        if Operation == 7:
            FDR = FaceDetector(grayScale(IMG, __FILE_WITH_EXTENSION).grayImg(), __FILE_WITH_EXTENSION)
            __RECT = FDR.imgDetect()
            for (x, y, w, h) in __RECT:
                __NEW_RECT = cv2.rectangle(IMG, (x, y), (x + w, y + h), (0, 255, 0), 2)
            Value = __NEW_RECT

        if Operation == 8:
            GDTC = genderDet(IMG, __FILE_WITH_EXTENSION)
            Value = GDTC.predict_gender(__FILE_WITH_EXTENSION, "frame")
            ImageCaption = GDTC.predict_gender(__FILE_WITH_EXTENSION, "label")

            # __technique = st.radio("Select one Blurring Algorithm", ('Canny', 'Sobel Laplace'))
            # if __technique == 'Canny':
            #     Value = DTE.imgCan("")
            # if __technique == 'Sobel Laplace':
            #     Value = DTE.imgSobLap("", grayScale(IMG, __FILE_WITH_EXTENSION).grayImg())

        # Saving processed image
        LI.imgSave(Value, FileNameWithoutExtension + __EXTENSION, "Images/")

        # st.image("Images/<FileNameWithoutExtension>" + __EXTENSION, width = 300)
        image_file = FileNameWithoutExtension + __EXTENSION
            
        # Saving Background removed image name with extension to a text file
        LI.imgSave(Value, image_file, "Images/")

        # colx, coly = st.columns(2)
        # with colx:
        #     # if Slider button is clicked
        #     x = st.button('Slider Image Comparision')
        # with coly:
        #     # if Parallel button is clicked
        #     y = st.button('Parallel Image Comparision?')
                
        with st.container():
            option = st.selectbox('',
                ('Image Comparision Method?', 'Parallel', 'Slider')
            )
            
            # if Download button is clicked
            # - open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "FileNameWithoutExtension" + __EXTENSION

            if option == 'Parallel':
                # Putting Columns based Viweing Experience if clicked on "Parallel Image Comparision?"
                col1, col2 = st.columns(2)
                with col1:
                    st.image("Images/upload" + __EXTENSION, caption = 'Original Image', width = 400)
                with col2:
                    st.image("Images/" + FileNameWithoutExtension + __EXTENSION, caption = ImageCaption, width = 400)
                st.success(SuccessMessage + "!!!")

            if option == 'Slider':
                c1, c2, c3 = st.columns([0.2, 0.6, 0.2])
                with c2:
                    # render image-comparison
                    image_comparison(
                        img1 = "Images/upload" + __EXTENSION,
                        img2 = "Images/" + FileNameWithoutExtension + __EXTENSION,
                        width = 400
                    )
                c1, c2, c3 = st.columns([0.32, 0.3, 0.38])
                with c2:
                    st.text('Original vs ' + ImageCaption)
                st.success(SuccessMessage + "!!!")    

            # Button to click and download image
            __UPLOAD = __PATH + FileNameWithoutExtension + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = FinalFileName + " " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                )

    except:
        st.error('Please upload an image in Upload Section')
        st.image("Images/help_imp.png", width = 300)

# Creates a sidebar navigation panel
with st.sidebar:
    selected = option_menu(
        "Tools", 
        ["About", "Upload", 'Remove Background', 'GrayScale', 'Edit Image', 'Detection'], 
        icons = ['info-circle-fill', 'file-earmark-arrow-up', 'wrench', '', '','person-bounding-box'], 
        menu_icon = "tools",
        default_index = 1
    )

# When "About" button is clicked on Side bar navigation panel
if selected == "About":
    # Creates a sidebar navigation panel
    with st.sidebar:
        choice = option_menu(
            "About", 
            ["Help", "Functions and Updates"], 
            icons = ['book-half', 'list-ol'], 
            menu_icon = "info-circle-fill"
        )

    # When "Help" button is clicked on Side bar navigation panel
    if choice == "Help":

        col1, col2 = st.columns(2)
        with col1:
            st.image('Images/logo.png', use_column_width = True)
        st.markdown("---")
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            st.caption("Step - 1 -> Click on Upload to upload an image")
            st.image("Images/help_upload.png", width = 200)
        with col2:
            st.caption("Step - 2 -> Click on Browse files and upload a desired file")
            st.image("Images/help_browse_button.png", width = 750)
        st.markdown("---")
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            st.caption("Step - 3 -> Click on an option such as \"Remove Background\" from Side panel to start selected processing style on an uploaded image")
            st.image("Images/help_option.png", width = 200)
        with col2:
            st.caption("Step - 4 -> Click on drop down Image Comparision Method and select a comparision method")
            st.image("Images/help_compare.png", width = 750)
            st.caption("Parallel - Comparision")
            st.image("Images/help_parallel_compare.png", width = 400)
            st.caption("Slider -  Comparision")
            st.image("Images/help_slider_compare.png", width = 400)
        st.markdown("---")
        st.caption("Step - 5 -> Click on download button to download desired image")
        st.image("Images/help_download.png", width = 150)
        st.markdown("---")
        st.warning("Note -> Before downloading you can view image to be downloaded")
        
    # When "Future Updates" button is selected
    if choice == "Functions and Updates":

        col1, col2 = st.columns(2)
        with col1:
            st.image('Images/logo.png', use_column_width = True)

        st.success("Welcome to Vivek's Image Manipulation Web Site")    
        st.text("1. Remove Unwanted Background including those sneaky and sticky people XD")
        st.text("2. Find Grayscale images to feel the black white days of 70s")
        st.text("3. Change - Rotate - Blurr - Detect Edge --- 4 in 1 solution found at Edit Image sub menu option")
        st.text("4. Detect number of humans in an image - Feeling ghosted already?")
        st.text("5. We are planning on many more easy and quick solutions so keep this website bookmarked!!!!")

# When "Upload" button is clicked on Side bar navigation panel
if selected == "Upload":

    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/logo.png', use_column_width = True)
    image_file = st.file_uploader("Upload Images", type = ["png", "jpg", "jpeg", "bmp"])
        
    if image_file is not None:
    # To See details
    # file_details = {"filename":image_file.name, "filetype":image_file.type, "filesize":image_file.size}
    # st.write(file_details)
        
        #Saving upload
        __EXTENSION = extensionFileName(image_file.name)
        with open(os.path.join("Images/", "upload" + __EXTENSION), "wb") as f:
        
        # with open(os.path.join("Images/Uploaded_Image", image_file.name), "wb") as f:
            f.write((image_file).getbuffer())
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.00000001)
                my_bar.progress(percent_complete + 1)
                if percent_complete == 99:
                    st.success("File Uploaded")
                    # To View Uploaded Image
                    # st.image(image_file, width = 250)
                    st.image(image_file, width = 300)
            
            # Writing file name into a text file
            text_file = open("texts/file_name.txt", "w") # open text file
            text_file.write(image_file.name) # write string to file
            text_file.close() # close file

    if not file_is_empty("texts/file_name.txt"):
        # open text file in read mode
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file
            
        # Loading file name from a text file
        __EXTENSION = extensionFileName(__FILE_NAME)

        # Remove Original Image
        # if remove_img("Images/", "upload" + __EXTENSION):
        #     # Print successfull deletion text
        #     st.title("Suceessfully removed Uploaded image, please upload images again!")
        #     st.balloons()
        remove_images(__EXTENSION)

    # Below Upload Button
    col1, col2, col3 = st.columns([0.45, 0.45, 0.1])
    with col2:
        st.caption("OR")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.text("Make use of below buttons")

    radio = st.radio("Make use of camera?", ('No', 'Yes'))
    __HELP = 'You can make use of top right corner left of url bar and change settings as well'
    
    # To Enable Camera Feed
    if radio == 'Yes':
        remove_images(__EXTENSION)
        img_file_buffer = st.camera_input("You look great! or do you?", disabled = False, help = __HELP)    
        if img_file_buffer is not None:
            # To read image file buffer with OpenCV:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite("Images/upload" + __EXTENSION, cv2_img)
    
    # To Disable Camera Feed
    if radio == 'No':
        st.camera_input("Camera Disabled Successfully", disabled = True, help = __HELP)

# Opeartions for fullMethod(operations = *)
# * is replaced by a number, 
# 1 - Remove Background
# 2 - Grayscale
# 3 - Translate/Displacement
# 4 - Rotate
# 5 - Blurr
# 6 - Edge Detection

# When "Remove Background" button is clicked on Side bar navigation panel
if selected == "Remove Background":

    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/logo.png', use_column_width = True)
    
    fullMethod(
        "bgremove", "Background Removed Image", 1, 
        "Background Removed", "Background Removed"
    )

# When "GrayScale" button is clicked on Side bar navigation panel
if selected == "GrayScale":

    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/logo.png', use_column_width = True)

    fullMethod(
        "grayscale", "Grayscale Image", 2, 
        "Grayscale Image generated", "Grayscale"
    )

# When "Edit Image" button is clicked on Side bar navigation panel
if selected == "Edit Image":
    
    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/logo.png', use_column_width = True)
        
    option = st.selectbox(
        'Which Opeartion to Perform?',
        ('None', 'Translate', 'Rotate', 'Blurr', 'Detect Edges')
    )

    # When "Translate" option is selected from Drop Down menu
    if option == 'Translate':
        fullMethod(
            "translate", "Move/Displace Image", 3, 
            "Image Moved/Displaced", "Moved_Displaced"
        )

    # When "Rotate" option is selected from Drop Down menu
    if option == 'Rotate':
        fullMethod(
            "rotate", "Rotated Image", 4,
            "Image Rotated", "Rotated"
        )

    # When "Blurr" option is selected from Drop Down menu
    if option == 'Blurr':
        fullMethod(
            "median", "Blurred Image", 5,
            "Image Blurred", "Blurred"
        )

    # When "Detect Edges" option is selected from Drop Down menu
    if option == 'Detect Edges':
        fullMethod(
            "detect", "Edge Detected Image", 6,
            "Image Edge Detected", "Edge Detected"
        )

# When "Detection" button is clicked on Side bar navigation panel
if selected == "Detection":
    
    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/logo.png', use_column_width = True)

    # Creates a sidebar navigation panel
    with st.sidebar:
        choice = option_menu(
            "Detection", 
            ["Face Detection", "Gender Detection"], 
            icons = ['person-circle', 'people-fill'], 
            menu_icon = "person-bounding-box"
        )
    
    # When "Face Detection" button is clicked on Side bar navigation panel
    if choice == "Face Detection":
        fullMethod(
            "detect", "Edge Detected Image", 7,
            "Image Edge Detected", "Edge Detected"
        )

    # When "Gender Detection" button is clicked on Side bar navigation panel
    if choice == "Gender Detection":
        fullMethod(
            "detect", "Gender Detected Image", 8,
            "Image Gender Detected", "Gender Based"
        )