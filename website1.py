# streamlit run website.py

# Installed Libraries
import streamlit as st
import streamlit_authenticator as stauth
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
from streamlit_image_comparison import image_comparison

# Utils
import time
import os
import streamlit as st
timestr = time.strftime("%Y%m%d-%H%M%S")

# Remove .streamlit from page title tag
st.set_page_config(
   page_title = "Vivek Vision",
   page_icon = "🧊",
   layout = "wide",
   initial_sidebar_state = "expanded",
)

names = ['Lazy Pingu','Racoon Chillin']
usernames = ['lpingu','racoonc']
passwords = ['Lp27031998#','rC27031998$']
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords, 
    'some_cookie_name', 'some_signature_key', cookie_expiry_days = 30
)

name, authentication_status, username = authenticator.login('Login', 'main')


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

# Method to incorporate multiple operations
def fullMethod(FileNameWithoutExtension, ImageCaption, Operation, TextToShow, SuccessMessage, FinalFileName):
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
            x = st.number_input('How much to be displaced - X Axis', min_value = -(IMG.shape[1]/2), max_value = (IMG.shape[1]/2))
            st.write('The current number is ', x, '(Negative, Postive - Left, Right)')
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

        # Saving processed image
        LI.imgSave(Value, FileNameWithoutExtension + __EXTENSION, "Images/")

        # st.image("Images/<FileNameWithoutExtension>" + __EXTENSION, width = 300)
        image_file = FileNameWithoutExtension + __EXTENSION
            
        # Saving Background removed image name with extension to a text file
        LI.imgSave(Value, image_file, "Images/")

        colx, coly = st.columns(2)
        # if Slider button is clicked
        with colx:
            x = st.button('Slider Image Comparision')
        # if Parallel button is clicked
        with coly:
            y = st.button('Parallel Image Comparision?')
                
        with st.container():
            if x:
                st.text("Images Comparision using Slider")
                # render image-comparison
                image_comparison(
                    img1 = "Images/upload" + __EXTENSION,
                    img2 = "Images/" + FileNameWithoutExtension + __EXTENSION,
                    width = 600
                )
                st.success(SuccessMessage + "!!!")
            elif y:
                # Putting Columns based Viweing Experience if clicked on "Parallel Image Comparision?"
                col1, col2 = st.columns(2)
                with col1:
                    st.text("Original Image - ")
                    st.image("Images/upload" + __EXTENSION, caption = 'Original Image', width = 400)
                with col2:
                    st.text(TextToShow + "Image - ")
                    st.image("Images/" + FileNameWithoutExtension + __EXTENSION, caption = ImageCaption, width = 400)
                st.success(SuccessMessage + "!!!")
            else:
                st.text(TextToShow + "Image - ")
                st.image("Images/" + FileNameWithoutExtension + __EXTENSION, caption = ImageCaption, width = 400)
                st.success(SuccessMessage + "!!!")
                
            # if Download button is clicked
            # - open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "FileNameWithoutExtension" + __EXTENSION
                
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
        st.image("Images/help.png")

if authentication_status:
    # Creates a sidebar navigation panel
    with st.sidebar.container():
        st.image('Images/logo.png', use_column_width = True)
    with st.sidebar:
        selected = option_menu(
            "Manipulation Menu", 
            ["Help", "Home Page", "Upload", 'Remove Background', 'GrayScale', 'Edit Image', 'Remove Images'], 
            icons = ['info-square', 'house-door', 'file-earmark-arrow-up', 'wrench', '', '', 'trash2'], 
            menu_icon = "cast", 
            default_index = 1,
        )
        selected

    # When "Help" button is clicked on Side bar navigation panel
    if selected == "Help":
        st.title("Help Site")
        st.markdown("---")
        st.header("Logout -> ")
        st.subheader("Go to Home then click on Logout button")
        st.image("Images/logout.png")
        st.markdown("---")
        st.markdown("---")
        st.header("Image Operation Tutotial ->")
        st.subheader("Step - 1 -> Click on Upload to upload an image")
        st.image("Images/help.png", width = 300)
        st.markdown("---")
        st.subheader("Step - 2 -> Click on Browse files and upload a desired file")
        st.image("Images/help1.png", width = 900)
        st.markdown("---")
        st.subheader("Step - 3 -> Click on an option such as \"Remove Background\" from Side panel to start selected processing style on an uploaded image")
        st.image("Images/help2.png", width = 300)
        st.markdown("---")
        st.subheader("Step - 4 -> Click on Either button to view images accordingly")
        st.image("Images/help3.png", width = 700)
        st.markdown("---")
        st.subheader("Step - 5 -> Click on download button to download desired image")
        st.image("Images/help4.png", width = 200)
        st.markdown("---")
        st.caption("Note -> Before downloading you can view image to be downloaded")

    if selected == "Home Page":
        col1, col2 = st.columns([5, 2])
        with col1:
            st.title("Welcome to Vivek's Image Manipulation Web Site")
        with col2:
            st.image('Images/logo.png', use_column_width = True)
        
        authenticator.logout('Logout ' + name, 'main')

        st.info("1. Remove Unwanted Background including those sneaky and sticky people XD")
        st.info("2. Find Grayscale images to feel the black white days of 70s")
        st.info("3. Change - Rotate - Blurr - Detect Edge --- 4 in 1 solution found at Edit Image sub menu option")
        st.info("4. No more use of uploaded photo? Do't worry we got it covered with fresh Remove Images option to throw them out")
        st.info("5. We are planning on many more easy and quick solutions so keep this website bookmarked!!!!")

    # When "Upload" button is clicked on Side bar navigation panel
    if selected == "Upload":
        st.title("Upload an Image")
        image_file = st.file_uploader("Upload Images", type = ["png", "jpg", "jpeg", "bmp"])
        if image_file is not None:
            # To See details
            # file_details = {"filename":image_file.name, "filetype":image_file.type, "filesize":image_file.size}
            # st.write(file_details)
            
            # To View Uploaded Image
            # st.image(image_file, width = 250)
            st.image(image_file, width = 300)
            
            #Saving upload
            __EXTENSION = extensionFileName(image_file.name)
            with open(os.path.join("Images/", "upload" + __EXTENSION), "wb") as f:
            
            # with open(os.path.join("Images/Uploaded_Image", image_file.name), "wb") as f:
                f.write((image_file).getbuffer())
                st.success("File Saved")
                
                # Writing file name into a text file
                text_file = open("texts/file_name.txt", "w") # open text file
                text_file.write(image_file.name) # write string to file
                text_file.close() # close file

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
        st.title("Removing Background!")
        fullMethod(
            "bgremove", "Background Removed Image", 1, 
            "Backgorund Removed ", "Background Removed", "Background Removed"
        )

    # When "GrayScale" button is clicked on Side bar navigation panel
    if selected == "GrayScale":
        st.title("GrayScale!")
        fullMethod(
            "grayscale", "Grayscale Image", 2, 
            "Grayscale ", "Grayscale Image generated", "Grayscale"
        )

    # When "Edit Image" button is clicked on Side bar navigation panel
    if selected == "Edit Image":
        st.title("Edit Uploaded Image!")
        
        option = st.selectbox(
            'Which Opeartion to Perform?',
            ('None', 'Translate', 'Rotate', 'Blurr', 'Detect Edges')
        )

        # When "Translate" option is selected from Drop Down menu
        if option == 'Translate':
            fullMethod(
                "translate", "Move/Displace Image", 3, 
                "Moved/Displaced ", "Image Moved/Displaced", "Moved_Displaced"
            )

        # When "Rotate" option is selected from Drop Down menu
        elif option == 'Rotate':
            fullMethod(
                "rotate", "Rotated Image", 4,
                "Rotated ", "Image Rotated", "Rotated"
            )

        # When "Blurr" option is selected from Drop Down menu
        elif option == 'Blurr':
            fullMethod(
                "median", "Blurred Image", 5,
                "Blurred ", "Image Blurred", "Blurred"
            )

        # When "Detect Edges" option is selected from Drop Down menu
        elif option == 'Detect Edges':
            fullMethod(
                "detect", "Edge Detected Image", 6,
                "Edge Detected ", "Image Edge Detected", "Edge Detected"
            )
            
    # When "Remove Images" button is clicked on Side bar navigation panel
    if selected == "Remove Images":
        # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file
                
            # Loading file name from a text file
            __EXTENSION = extensionFileName(__FILE_NAME)

            # Remove Original Image
            if remove_img("Images/", "upload" + __EXTENSION):
                # Print successfull deletion text
                st.title("Suceessfully removed Uploaded image, please upload images again!")
                st.balloons()

            # Remove "Background removed" image
            remove_img("Images/", "bgremove" + __EXTENSION)
            
            # Remove "Grayscale" image
            remove_img("Images/", "grayscale" + __EXTENSION)
            
            # Remove "Translate" image
            remove_img("Images/", "translate" + __EXTENSION)

            # Remove "Rotate" image
            remove_img("Images/", "rotate" + __EXTENSION)

            # Remove "Blurr" image
            remove_img("Images/", "median" + __EXTENSION)

            # Remove "Detected Edge" image
            remove_img("Images/", "detect" + __EXTENSION)

        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")
    
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    
    elif authentication_status == None:
        st.warning('Please enter your username and password')