import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import cv2
from img_gridder import get_row_image
import json
from answer_key import answer_key_setter
from folder_selector import folder_selector
# import OpenImageIO as oiio

st.set_option('deprecation.showfileUploaderEncoding', False)


tab1, tab2, tab3 = st.tabs(["SetUp Template", "Answer Key", "Load The Folder"])

# Upload an image and set some options for demo purposes
with tab1:
    st.header("Template SetUp")
    st.sidebar.header("SetUp")
    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg', 'tiff', 'jpeg'])
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
        FILE_TYPE = img_file.name.split(".")[-1]
        print(FILE_TYPE)
        img = Image.open(img_file)
        #resize the image
        img = img.resize((1000,1000),Image.LANCZOS)
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
            
            maxsize = (250,150)

            
            if FILE_TYPE != "tif" and FILE_TYPE != "tiff":
                # print(row_image)
                row_image = cv2.resize(row_image,maxsize,interpolation=cv2.INTER_AREA)
                st.image(row_image)
            else:
                # print(row_image)
                row_image = Image.fromarray(row_image)
                row_image.thumbnail(maxsize, Image.LANCZOS)
                st.image(row_image)

        # with open('roi.json', 'r') as f:
        #     ROI_list = json.load(f)
        # st.write(ROI_list[0][0])
        

with tab2:
        
    try:
        NUMBER_OF_ROWS = []
        for i in range(Number_of_Column_Groups):
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            num_rows = ROI_list[i][2]
            NUMBER_OF_ROWS.append(num_rows)
            max_num_rows = max(NUMBER_OF_ROWS)
            df = answer_key_setter(Number_of_Column_Groups, num_rows=max_num_rows)
            # st.write(Number_of_Column_Groups)
            # st.write(df["A"])
            # st.write(df.columns)
            for j in range(Number_of_Column_Groups):
                # st.write(ROI_list[j][2])
                # st.write(letters[j])
                st.write(df[letters[j]].iloc[:ROI_list[j][2]])
                
    except:
        pass


with tab3:
    folder_name = folder_selector()
    st.code(folder_name)