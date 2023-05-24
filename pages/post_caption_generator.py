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

st.write("Captions that turn your images into attention-grabbing Instagram posts.")
form = st.form(key='my_form')
platform = form.multiselect(label="Platform :red[*]", options=["Instagram", "Facebook", "Twitter",
                                                               "Linkedin", "Pinterest"])
description = form.text_input(label="Description :red[*]", placeholder="a post about baked vs fried potatoes")
tone = form.text_input(label="Tone of voice", placeholder="serious")

if form.form_submit_button("Generate"):
    if str.strip(description) == "" or len(platform) == 0:
        st.error("Please enter the required field")
    else:
        prompt = f"I want you to act as a professional social media content creator, and I'm looking for " \
                 f"attention-grabbing captions that can turn images into captivating Instagram posts." \
                 f"To assist you, the post description is '{description}', " \
                 f"{'the tone is ' + tone if tone != '' else ''}" \
                 f", With this information, craft engaging captions that resonate with {', '.join(platform)} audience."

        with st.spinner("Generating.."):
            res = generate(prompt)
            st.divider()
            st.header("🏷️Captions")
            st.write(res)
