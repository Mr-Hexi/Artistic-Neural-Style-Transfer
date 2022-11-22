import base64
import json
from pathlib import Path
import matplotlib.pyplot as plt
import requests
import streamlit as st


def image_to_data_url(filename, img=None):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    if img is not None:
        encode = base64.b64encode(img).decode('utf-8')
    else: 
        encode = base64.b64encode(open(filename, "rb").read()).decode('utf-8')
    encode = prefix+encode
    return encode 
    
    
    
def style_transfer(content_img,style_image, style_weight = 1, content_weight = 1, style_blur=False):
    pass

st.set_page_config(page_title="ArtisticNeural Style Transfer 🏞️",
                  page_icon="🖼️",
                  initial_sidebar_state="expanded",
                  # layout="wide"
                  )

st.title("Artistic Neural Style Transfer 📸")
st.markdown("**Neural style transfer is a technique of blending style of a content image and a style image together so the output image looks like the content image, but “painted” in the style of the style reference image.** [Learn More](https://www.tensorflow.org/tutorials/generative/style_transfer)")

options = ["Upload your own Style Image",
           "StarryNight",
            "StarryNight2",
            "Scream",
            "Picasso1",
            "Picasso2",
            "Picasso3",
            "Picasso4",
            "Picasso5",
            "Picasso6",
            "Chromoluminarism",
            "The-Bedroom",
            "The Great Wave",
            "Lines",
            "Sketch1",
            "Sketch2",
            ]

with st.sidebar:
    with open("design.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    box = st.selectbox("Select Style",
                 options=options, index=1)
    
    style_path = [img_path.stem for img_path in Path("examples").glob('**/*')]
        
    if "Upload" in box:
        style_upload = st.file_uploader(label="Chosse an Style Image", key=1)
        if style_upload:
            img = style_upload.read()
            st.image(img, width=150)
        style_img = image_to_data_url(style_upload.name,img)    
    elif box in style_path:
            img  = "examples\{}.jpg".format(box)
            st.image(plt.imread(img), width=150) 
            style_img = image_to_data_url(img)    
        
    
        

    slider_1 = st.slider("Adjust Style Density", min_value=0.0,max_value=2.0,step=0.01,value=1.0)
    slider_2 = st.slider("Content Sharpness", min_value=1.0,max_value=5.0,step=0.01,value=1.0)
    checkbox = st.checkbox("Tune Style(experimental)")
    

  
  
    



    
upload_file = st.file_uploader(label="Choose a image file ")    
if upload_file:

    img = upload_file.read()
    content_img=  upload_file.name
    content_img= image_to_data_url(content_img, img)
    st.info("Content Image")
    st.image(img, width=300)
    
    
    if st.sidebar.button("Submit"):
        r = requests.post(url="https://hexii-neural-style-transfer.hf.space/api/predict",
        json = {
        "data": [
            content_img,
            style_img,
            slider_1,
            slider_2,
            checkbox,
        ]})
        data= r.json()
        data = data['data'][0]
        data  =data.split(",")[1]
        image = base64.b64decode(data)
        
        st.success(f"Stylized Image: ")
        st.image(image) 
        col2.download_button("Download Image", data=content_img ,file_name="Stylized_image.jpg",mime="image/jpg")
