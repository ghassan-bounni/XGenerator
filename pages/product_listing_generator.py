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

st.write("Generate product listings that are SEO optimized")
form = st.form(key="my_form")
product_selling = form.text_input(
    label="What do you want to sell? :red[*]", placeholder="Nike Air Max 90"
)
product_description = form.text_input(
    label="Small Description :red[*]", placeholder="A pair of Nike Air Max 90"
)
platform = form.multiselect(
    label="Platform :red[*]", options=["Amazon", "Ebay", "Shopify", "Etsy"]
)

if form.form_submit_button(label="Generate"):
    if (
        str.strip(product_selling) == ""
        or str.strip(product_description) == ""
        or len(platform) == 0
    ):
        st.error("Please enter the required field")
    else:
        prompt = (
            f"Your role will be that of an {platform} expert, providing guidance to sellers on crafting effective {platform} listings."
            f" You'll produce an {platform} listing that is optimized for SEO. "
            "Including Name of the shop, Title, Category, Product Description, Key Features, 20 key words up to 20 characters"
            f" taking into consideration this information about the seller:  selling {product_selling} with the following description: {product_description}."
        )

        with st.spinner("Generating..."):
            res = generate(prompt)
            st.divider()
            st.header("📄Product Listing")
            st.write(res)
