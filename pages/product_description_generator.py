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

st.write("Generate product descriptions that rank high on searches and convert visitors into customers.")

form = st.form(key='my_form')
product_name = form.text_input(label="Product name :red[*]", placeholder="potato chips")
product_description = form.text_input(label="Product description / characteristics :red[*]",
                                      placeholder="a bag of potato chips, crispy, salty and crunchy")
tone = form.text_input(label="Tone of voice", placeholder="serious")
keywords = form.text_input(label="Keywords", placeholder="potato chips, potato, chips, crispy, salty, crunchy")
platform = form.multiselect(label="Platform :red[*]", options=["Amazon", "Etsy", "Shopify", "Walmart", "Target"])

if form.form_submit_button("Generate"):
    if str.strip(product_name) == "" or str.strip(product_description) == "" or len(platform) == 0:
        st.error("Please fill the required field")
    else:
        prompt = f"I want you to act as a professional copywriter, and I'm looking for a product description " \
                 f"that rank high on searches and convert visitors into customers. To assist you, " \
                 f"the product name is '{product_name}', the product description is '{product_description}'" \
                 f"{', the tone is ' + tone if str.strip(tone) != '' else ''}" \
                 f"{', and the keywords are' + keywords if str.strip(keywords) != '' else ''}" \
                 f", With this information, craft a product description that resonates with {', '.join(platform)} audience."

        with st.spinner("Generating.."):
            res = generate(prompt)
            st.divider()
            st.header("🏷️Product description")
            st.write(res)
