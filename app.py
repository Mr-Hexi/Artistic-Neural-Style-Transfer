import base64
import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import requests
import streamlit as st
from gradio_client import Client, handle_file


def image_to_data_url(filename, img=None):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    if img is not None:
        encode = base64.b64encode(img).decode('utf-8')
    else: 
        encode = base64.b64encode(open(filename, "rb").read()).decode('utf-8')
    encode = prefix+encode
    return encode 


# Create temp directory to store uploaded files
os.makedirs("temp", exist_ok=True)

st.set_page_config(
    page_title="ArtisticNeural Style Transfer 🏞️",
    page_icon="🖼️",
    initial_sidebar_state="expanded"
)

st.title("Artistic Neural Style Transfer 📸")
st.markdown(
    "**Neural style transfer is a technique of blending style of a content image and a style image together so the output image looks like the content image, but “painted” in the style of the style reference image.** "
    "[Learn More](https://www.tensorflow.org/tutorials/generative/style_transfer)"
)

# --------- Content Image Upload ---------
content_img_path = None
upload_file = st.file_uploader(label="Choose a content image")    
if upload_file:
    img = upload_file.read()
    content_img_path = f"temp/{upload_file.name}"
    print(content_img_path)
    with open(content_img_path, "wb") as f:
        f.write(img)
    st.info("Content Image")
    st.image(img, width=300)

# --------- Style Selection ---------
options = [
    "Upload your own Style Image",
    "StarryNight", "StarryNight2", "Scream",
    "Picasso1", "Picasso2", "Picasso3", "Picasso4", "Picasso5", "Picasso6",
    "Chromoluminarism", "The-Bedroom", "The Great Wave", "Lines", "Sketch1", "Sketch2"
]

style_img_path = None

with st.sidebar:
    with open("design.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    box = st.selectbox("Select Style", options=options, index=1)

    style_path_list = [img_path.stem for img_path in Path("examples").glob('**/*')]

    if "Upload" in box:
        style_upload = st.file_uploader(label="Choose a style image", key=2)
        if style_upload:
            style_img_data = style_upload.read()
            style_img_path = f"temp/{style_upload.name}"
            with open(style_img_path, "wb") as f:
                f.write(style_img_data)
            st.image(style_img_data, width=150)

    elif box in style_path_list:
        style_img_path = f"examples/{box}.jpg"
        st.image(plt.imread(style_img_path), width=150)

    slider_1 = st.slider("Adjust Style Density", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
    slider_2 = st.slider("Content Sharpness", min_value=1.0, max_value=5.0, step=0.01, value=1.0)
    checkbox = st.checkbox("Tune Style (experimental)")

# --------- Submit to Hugging Face Model ---------
if st.sidebar.button("Submit"):
    if content_img_path and style_img_path:
        try:
            st.info("Processing... This may take a few seconds.")
            client = Client("Hexii/Neural-Style-Transfer")
            result = client.predict(
                content_img=handle_file(content_img_path),
                style_image=handle_file(style_img_path),
                style_weight=slider_1,
                content_weight=slider_2,
                style_blur=checkbox,
                api_name="/predict"
            )

            st.success("Stylized Image:")
            st.image(result)

            with open(result, "rb") as f:
                img_bytes = f.read()

            st.download_button(
                "Download Stylized Image",
                data=img_bytes,
                file_name="Stylized_image.jpg",
                mime="image/jpg"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please upload both content and style images before submitting.")
