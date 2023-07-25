import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import cv2
st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes
st.header("Cropper Demo")
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
Number_of_Column_Groups = st.sidebar.number_input(label="Number of Coulmn Groups", min_value=1, max_value=10, value=1, step=1)
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

if img_file:
    img = Image.open(img_file)
    if not realtime_update:
        st.write("Double click to save crop")
    # Get a cropped image from the frontend
    for i in range(Number_of_Column_Groups):

        cropped_img= st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                    aspect_ratio=aspect_ratio,return_type='box',key=i)
        left, top, width, height = cropped_img['left'], cropped_img['top'], cropped_img['width'], cropped_img['height']
        # print(cropped_img)
        # st.write(cropped_img)
        # st.write(left, top, width, height)
        img = img.crop((left, top, left+width, top+height))
        st.image(img)
        # for i in range(Number_of_Column_Groups):
        # _ = cropped_img.thumbnail((150,150))
        # st.image(cropped_img)
