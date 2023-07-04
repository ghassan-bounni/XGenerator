import streamlit as st
from st_pages import add_page_title
from utils import generate

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

st.write("Generate ad headlines to increase conversion rate")

form = st.form(key="my_form")
product = form.text_input(label="Product :red[*]", placeholder="Buddha’s Blend Sachets")
description = form.text_input(
    label="Description :red[*]",
    placeholder="fresh, delicate mix of white and green tea with jasmine pearls "
    "for a sweet floral perfume.",
)
keywords = form.text_input(
    label="Target Keywords :red[*]",
    placeholder="tea, green tea, jasmine tea, white tea, loose leaf tea",
)

if form.form_submit_button("Generate"):
    if (
        str.strip(product) == ""
        or str.strip(description) == ""
        or str.strip(keywords) == ""
    ):
        st.error("Please enter the required field")
    else:
        prompt = (
            f"I want you to act as a professional copywriter, and I'm looking for ad headlines for a new "
            f"product. The product is {product}, having the following description {description}. The target keywords are {keywords}. "
            f"Using this information, write 5 ad headlines that will increase conversion rate."
        )

        with st.spinner("Generating.."):
            res = generate(prompt)
            st.divider()
            st.header("🏷️Ad Headlines")
            st.write(res)
