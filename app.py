# Import required libraries

import cv2
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
import os

# Home UI 

def main():

    st.set_page_config(
        layout="wide"
    )

    tabs = st.sidebar.selectbox(
        'Choose one of the following',
        ('Annotate Image','Resize Image'),
        key="main_menu"
    )

    # UI Options  
    if tabs == 'Annotate Image':
        annotateImg()
    if tabs == 'Resize Image':
        resizeImg()

# Pre-process Image
def preProcessImg(img, new_height=480):
    # Pre-processing image: resize image
    height, width, _ = img.shape
    width = int(new_height/height*width)
    img = cv2.resize(img,(width,new_height))
    return img

# Upload Image
def uploadImage(key, new_height=480):

    uploaded_file = st.file_uploader("Choose a Image file",key=key)
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        # Pre-processing image: resize image
        return preProcessImg(img, new_height)
    
    return cv2.cvtColor(preProcessImg(cv2.imread('sample.jpg'),new_height),cv2.COLOR_BGR2RGB)

# About Me UI 
def annotateImg():
    st.header("Annotate Image")

    img = uploadImage("annotation_img")

    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ( "rect", "point", "freedraw", "line", "circle", "transform")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ", "#5FCE42")

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Create a canvas component
    st_canvas(
        fill_color="rgba(0, 0, 0, 0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=Image.fromarray(img),
        update_streamlit=realtime_update,
        height=img.shape[0],
        width=img.shape[1],
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="annotation_canvas",
    )

def resizeImg():
    st.header("Resize Image")

    img = uploadImage("resize_img")

    scaleFactor = st.slider("Times Image",1,10,1,1,key='resize')/5
    scaledImg = cv2.resize(img, None, fx=scaleFactor, fy = scaleFactor, interpolation = cv2.INTER_LINEAR)

    st.image(scaledImg)
    pass

if __name__ == "__main__":
    main()