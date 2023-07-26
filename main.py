import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import cv2
from img_gridder import get_row_image
import json
st.set_option('deprecation.showfileUploaderEncoding', False)


tab1, tab2, tab3 = st.tabs(["Set Up", "Dog", "Owl"])

# Upload an image and set some options for demo purposes
with tab1:
    st.header("Cropper Demo")
    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    # aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    Number_of_Column_Groups = st.sidebar.number_input(label="Number of Coulmn Groups", min_value=1, max_value=10, value=1, step=1)
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict['Free']

    if img_file:
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        ROI_list = []
        for i in range(Number_of_Column_Groups):

            cropped_img, rect = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                        aspect_ratio=aspect_ratio,key=i,return_type='image')
            
            x, y, width, height = rect['left'], rect['top'], rect['width'], rect['height']

            roi = (x, y, width, height)
            # st.write(x, y, width, height)
            try:
                num_columns = st.number_input(label="Number of Columns", min_value=1, max_value=100, value=4, step=1, key=x+y)
                
                num_rows = st.number_input(label="Number of Rows", min_value=1, max_value=100, value=1, step=1, key=x*y)

                row_number = st.number_input(label="Row Number", min_value=1, max_value=num_rows, value=1, step=1, key=x/y)
            except:
                st.write("Please select a region")
                
            ROI_list.append((roi, num_columns, num_rows))
            row_image = get_row_image(img, num_columns, num_rows, row_number, roi)
            # Save the ROI for each region as a json file
            with open('roi.json', 'w') as f:
                json.dump(ROI_list, f)
            # load the ROI from the json file
            maxsize = (250,150) 
            row_image = cv2.resize(row_image,maxsize,interpolation=cv2.INTER_AREA)
            st.image(row_image)


        # with open('roi.json', 'r') as f:
        #     ROI_list = json.load(f)
        # st.write(ROI_list[0][0])
        