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

st.write("Write SEO optimized articles based on provided topic and reference link")
form = st.form(key='my_form')
topic = form.text_input(label="Article Topic :red[*]", placeholder="machine learning in finance, healthy eating "
                                                                   "habits, etc.")
reference = form.text_input(label="Reference Article (optional)", placeholder="https://www.example.com/article")
if form.form_submit_button(label='Generate'):
    with st.spinner("Generating..."):
        if topic == '':
            st.error("Please enter a topic")
        else:
            prompt = f"I want you to act as a professional writer, using the topic '{topic}'" \
                     f"{f', and this article for reference {reference}, ' if reference != '' else ''}" \
                     f"write a professional article and make it seo optimized"

            response = generate(prompt)
            st.divider()
            st.write("## Generated Article :memo:")
            st.markdown(response, unsafe_allow_html=True)
