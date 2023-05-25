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

st.write("A social media content plan that will help you create engaging content for your audience!")
form = st.form(key='my_form')

objective = form.text_input(label="Objective :red[*]", placeholder="increase brand awareness, drive website traffic, "
                                                                   "promote a product/service, etc.")
description = form.text_input(label="Description :red[*]", placeholder="a smartwatch that can track your heart rate, an app that tracks your "
                                                                       "expenses, etc.")
platform = form.multiselect(label="Platform :red[*]", options=["Instagram", "Facebook", "Twitter",
                                                               "Linkedin", "Pinterest"])
target_audience = form.multiselect(label="Target Audience :red[*]", options=["Millennials", "Gen Z", "Gen X",
                                                                             "Baby Boomers"])
interests = form.text_input(label="Interests", placeholder="Artificial Intelligence, Fashion, etc.")
location = form.text_input(label="Location", placeholder="United States, United Kingdom, etc.")
content_theme = form.text_input(label="Content Theme :red[*]", placeholder="industry-related news, tips and tutorials, "
                                                                           "behind-the-scenes glimpses, "
                                                                           "customer testimonials, etc.")
posting_frequency = form.text_input(label="Posting Frequency :red[*]", placeholder="once a day, twice a week, etc.")

if form.form_submit_button("Generate"):
    if str.strip(objective) == '' or str.strip(description) == '' or len(platform) == 0 or len(target_audience) == 0 \
            or str.strip(content_theme) == '' or str.strip(posting_frequency) == '':
        form.error("Please fill the required fields")
        pass
    else:
        prompt = f"i want you to act as a pro social media manager and content creator and i want you to create a social media content " \
                 f"plan that will help me create engaging content for your audience," \
                 f"the objective is to {objective}, " \
                 f"the description is {description}, " \
                 f"the platforms are '{', '.join(platform)}', " \
                 f"the target audience is '{', '.join(target_audience)}', " \
                 f"{'interested in ' + interests + ', ' if str.strip(interests) != '' else ''}" \
                 f"{'located in ' + location + ', ' if str.strip(location) != '' else ''}" \
                 f"the content theme is '{content_theme}'. " \
                 f"provide also a 4-week monthly calendar with a {posting_frequency} posting frequency."

        with st.spinner("Generating..."):
            res = generate(prompt)

        st.divider()
        st.header("🕑Content Plan:")
        st.markdown(res, unsafe_allow_html=True)
