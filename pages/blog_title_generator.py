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

form = st.form(key='my_form')
blog_idea = form.text_input(label="Blog Idea :red[*]", placeholder="Artificial intelligence in Copywriting")

if form.form_submit_button("Generate"):

    if blog_idea == "":
        form.error("Please fill the required fields")
    else:
        prompt = f"I want you to act as a professional blogger and help me generate captivating blog titles " \
                 f"based on a simple idea.The idea revolves {blog_idea}.With your expertise," \
                 f" I believe we can create compelling titles that will grab readers' attention and inspire them " \
                 f"to take action. Let's work together to craft engaging titles that will drive traffic to my blog."

        with st.spinner("Generating..."):
            res = generate(prompt)

        st.divider()
        st.header("🪧Titles:")
        st.write(res)
