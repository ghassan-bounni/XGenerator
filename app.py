import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="XGenerator", page_icon="🧠")
show_pages_from_config()
add_page_title()

st.markdown("""
<style>
footer {visibility : hidden;}
</style>
""", unsafe_allow_html=True)
