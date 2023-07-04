import io
import os
import requests
import streamlit as st
from PIL import Image
from st_pages import add_page_title
from constants import car_style_dict
from utils import (
    prepare_prompt,
    upload_file,
    generate_sd_img,
    generate_sd_controlnet_img,
)

st.set_page_config(page_title="XGenerator", page_icon="🧠")
add_page_title()

st.markdown(
    """
<style>
footer {visibility : hidden;}
</style>
""",
    unsafe_allow_html=True,
)

st.write("Create artistic images of different kinds of vehicles")

brand = st.text_input(label="Brand :red[*]", placeholder="Tesla, BMW, Audi, etc.")
model = st.text_input(label="Model :red[*]", placeholder="Model S, Model 3, etc.")
year = st.text_input(label="Year (optional)", placeholder="2019, 2020, etc.")
cols = st.columns(2)
style = cols[0].selectbox(label="Style :red[*]", options=car_style_dict.keys())
cols[1].image(f"assets/collage_{str.lower(style)}.jpg", caption="Style Examples")
color = st.text_input(
    label="Color (optional)", placeholder="Red, Blue, Green body and black seats etc."
)
background = st.text_input(
    label="Background (optional)", placeholder="City, Forest, etc."
)
init_image = st.file_uploader(
    label="Initial Image to use as reference (optional, aspect ratio: 3:2, :red[copies pose and special mods])",
    type=["png", "jpg", "jpeg"],
)
images = []

if st.button(label="Generate"):
    with st.spinner(text="Generating..."):
        if str.strip(brand) != "" and str.strip(model) != "":
            prompt = prepare_prompt(brand, model, year, style, color, background)

            if init_image:
                img = Image.open(init_image)
                if img.size[0] / img.size[1] != 3 / 2:
                    st.error("Please upload an image with an aspect ratio of 3:2")
                    st.stop()

                img.save(init_image.name)
                success, url = upload_file(init_image.name)
                os.remove(init_image.name)

                if success:
                    img_url = url
                else:
                    st.error(
                        "Something went wrong while uploading the image, please try again."
                    )
                    st.stop()

                images = [
                    Image.open(requests.get(url, stream=True, timeout=300).raw)
                    for url in generate_sd_controlnet_img(prompt, 768, 512, img_url)
                ]
            else:
                images = [
                    Image.open(requests.get(url, stream=True, timeout=300).raw)
                    for url in generate_sd_img(prompt, 768, 512)
                ]

        else:
            st.error("Please fill in the required fields marked with red asterisk [*]")

if images:
    st.divider()
    st.header("Generated Images")
    img_cols = st.columns(3)
    for i in range(3):
        img_cols[i].image(images[i], use_column_width=True)
        image_bytes = io.BytesIO()
        # Save the PIL image as bytes in the BytesIO object
        images[i].save(image_bytes, format="PNG")
        img_cols[i].download_button(
            label="Download",
            data=image_bytes,
            file_name=f"generated_img_{i}.png",
            mime="image/png",
        )
