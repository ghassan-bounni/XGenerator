import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from constants import PAGES
from components import page_card

st.set_page_config(page_title="XGenerator", page_icon="🧠", initial_sidebar_state="collapsed")
show_pages_from_config()
add_page_title()

st.markdown("""
<style>
footer {visibility : hidden;}
</style>
""", unsafe_allow_html=True)

sections = PAGES.keys()

for section in sections:
    st.subheader(section)
    cols = st.columns(3)
    for i, page in enumerate(PAGES[section]):
        with cols[i % 3]:
            page_card(page["title"], page["description"], page["url"] if "url" in page else None)