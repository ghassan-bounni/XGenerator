import io
import requests
import streamlit as st
from st_pages import add_page_title
from PIL import Image
from utils import upscale

st.set_page_config(page_title="XGenerator", page_icon="🧠")
add_page_title()

st.markdown("""
<style>
footer {visibility : hidden;}
</style>
""", unsafe_allow_html=True)

st.write("Upscale your images to be print ready with AI - ")

switch = st.radio("Paste Image url or Upload an Image", options=["url", "img"])

img_input = st.text_input(label="Image url :red[(We only accept images with aspect ratio 2:3 / 3:2 or 1:1)]",
                          placeholder="https://example.com/img1.png") if switch == "url"\
    else st.file_uploader(label="Upload Image :red[(We only accept images with aspect ratio 2:3 / 3:2 or 1:1)]",
                          accept_multiple_files=True, type=["png", "jpg", "jpeg"])

images = []
if st.button("upscale"):
    with st.spinner("Upscaling..."):
        if img_input and switch == "url":

            if str.strip(img_input) == "":
                st.error("Please enter a valid image url")
                st.stop()

            if img_input.startswith("https://drive.google.com"):
                file_name = img_input.split("/")[-1].replace(" ", "")
                img_input = "https://drive.google.com/uc?export=download&id=" + img_input.split("/")[-2]

            elif not img_input.endswith((".png", ".jpg", ".jpeg")):
                st.error("Please enter a valid image url")
                st.stop()

            img = Image.open(requests.get(img_input, stream=True).raw)

            aspect_ratio = img.size[0] / img.size[1]
            if aspect_ratio not in [2 / 3, 3 / 2, 1.0]:
                st.error("Please paste an image url with aspect ratio 2:3 / 3:2 or 1:1")
                st.stop()

            if img.size < (512, 512):
                st.error("Please paste an image url with minimum size of 512x512")
                st.stop()
            elif img.size > (1500, 1500):
                st.error("Please paste an image url with maximum size of 1500x1500")
                st.stop()

            st.image(img, use_column_width=True)

            images.append(upscale(img, aspect_ratio, file_name))

        elif img_input and switch == "img":
            cols1 = st.columns(3)

            for i, image_file in enumerate(img_input):
                image = Image.open(image_file)
                aspect_ratio = image.size[0] / image.size[1]

                if aspect_ratio not in [2 / 3, 3 / 2, 1.0]:
                    st.error("Please upload an image with aspect ratio 2:3 / 3:2 or 1:1")
                    st.stop()

                if image.size < (512, 512):
                    st.error("Please upload an image with minimum size of 512x512")
                    st.stop()
                elif image.size > (1500, 1500):
                    st.error("Please upload an image with maximum size of 1500x1500")
                    st.stop()

                img = cols1[i % 3].image(image, use_column_width=True)
                images.append(upscale(image, aspect_ratio, image_file.name.replace(" ", "")))

if images:
    st.subheader("Upscaled Images")
    cols2 = st.columns(len(images) if len(images) < 3 else 3)
    for i, image in enumerate(images):
        cols2[i % 3].image(image, use_column_width=True)

        image_bytes = io.BytesIO()
        # Save the PIL image as bytes in the BytesIO object
        image.save(image_bytes, format='PNG')

        cols2[i % 3].download_button(label="Download", data=image_bytes, file_name=f"upscaled_image_{i}.png", mime="image/png")
