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

st.write("Generate custom and personalized letters for any occasion")

form = st.form("my-form")
sender = form.text_input("Who is it from? :red[*]", placeholder="your name, your nickname, etc.")
target = form.text_input("Who is it for? (add your relation to this person, use a nickname if you want) "
                         ":red[*]",
                         placeholder="lil' bits my best friend, my baby boo, my mom , my boyfriend Johnny, "
                                     "etc.")
occasion = form.text_input("What is the occasion? :red[*]",
                           placeholder="birthday, anniversary, Father's Day, etc.")
tone = form.text_input("What is the tone of the letter? :red[*]", placeholder="funny, serious, etc.")
# optional selection
memory = form.text_input("What is your favorite memory with this person? (optional, "
                         "don't start with my favorite memory is)",
                         placeholder="skydiving, summer camp, fishing trip, etc.")

descriptive_words = form.text_input("What words best describe the recipient of this letter?  "
                                    "(optional, comma separated)",
                                    placeholder="kind, funny, smart, etc.")

if form.form_submit_button("Generate"):
    if str.strip(sender) == "" or str.strip(target) == "" or str.strip(occasion) == "" or str.strip(tone) == "":
        form.error("Please fill in all required fields")

    else:
        prompt = f"write a {tone} message for {occasion} to {target}"\
                    f"{', my favorite memory of this person is ' + memory if str.strip(memory) != '' else ''}"\
                    f"{', I think he is ' + descriptive_words if str.strip(descriptive_words) != '' else ''}"\
                    f", Please keep the message concise, between 140 and 200 words. my name is {sender}."

        with st.spinner("Generating..."):
            response = generate(prompt)

        st.divider()
        st.write("## Generated Letter :memo:")
        st.markdown(response, unsafe_allow_html=True)
