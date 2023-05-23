import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from utils import generate

st.set_page_config(page_title="XGenerator", page_icon="🧠")
show_pages_from_config()
add_page_title()

st.markdown("""
<style>
footer {visibility : hidden;}
</style>
""", unsafe_allow_html=True)

blog_idea = st.text_input(label="Blog Idea :red[*]", placeholder="Artificial intelligence in Copywriting")

if st.button("Generate Blog Titles"):

    if blog_idea == "":
        st.error("Please fill the required fields")

    prompt = f"I want you to act as a professional blogger and help me generate captivating blog titles based on a simple idea.\
             The idea revolves {blog_idea}. " \
             "With your expertise, I believe we can create compelling titles that will grab readers' attention and " \
             "inspire them to take action. Let's work together to craft engaging titles that will drive traffic to my blog."

    res = generate(prompt)
    st.header("🪧Titles:")
    st.write(res)
