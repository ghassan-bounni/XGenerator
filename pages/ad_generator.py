import streamlit as st
from st_pages import add_page_title
from utils import generate

st.set_page_config(page_title="XGenerator", page_icon="🧠")
add_page_title()

st.markdown("""
<style>
footer {visibility : hidden;}
</style>
""", unsafe_allow_html=True)

st.write("Generate ads that will help you sell your products")

form = st.form(key='my_form')
product_name = form.text_input(label="Product Name :red[*]", placeholder="a smartwatch, a pair of shoes, etc.")
description = form.text_input(label="Description :red[*]", placeholder="a smartwatch that can track your heart rate")
platform = form.selectbox(label="Platform :red[*]", options=["Facebook", "Google", "Linkedin"])
occasion = form.text_input(label="Occasion (optional)", placeholder="gaming tournaments, a birthday, a wedding, etc.")
promo = form.text_input(label="Promo (optional, Format: your code % off)", placeholder="e.g YAS50 50% off")
emoji = form.checkbox(label="Use Emojis (optional)", value=False)

if form.form_submit_button("Generate"):
    if product_name == "" or description == "":
        st.error("Please fill the required fields")
    else:
        prompt = f"Create a captivating and interactive {platform} ad copy with a maximum of 100 tokens." \
                 f"You should consider the product name {product_name}, with it's description {description}." \
                 f"{f' Incorporate the {occasion}.' if occasion != '' else ''}" \
                 f"{f' and the promo code {promo}.' if promo != '' else ''}" \
                 f"{f' Use appropriate emojis.' if emoji else ''}"

        with st.spinner("Generating..."):
            res = generate(prompt)
            st.divider()
            st.header(f"🎞️{platform} Ad:")
            st.write(res)
