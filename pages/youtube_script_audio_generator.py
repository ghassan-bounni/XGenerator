import streamlit as st
from st_pages import add_page_title
from utils import (
    generate,
    script_to_audio,
    check_audio_length,
    clone_voice,
    check_cloned_voice,
)

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

st.write("Generate an Audio script for your YouTube video with AI")
form = st.form(key="form")
title = form.text_input(
    "Enter the video's title :red[*]",
    placeholder="Essential Tips for Successful Job Interviews, Quick and Easy Dinner Recipes for Busy Parents, etc...",
)
description = form.text_input(
    "Enter the video's description :red[*]",
    placeholder="From preparation to body language, we'll guide you towards landing your dream job",
)
search_term = form.text_input(
    "Enter search term (optional)",
    placeholder="job interview tips, how to succeed in interviews, interview prep, etc...",
)

tone = form.text_input(
    "Enter tone of voice :red[*]",
    placeholder="Supportive, empowering, informative, etc...",
)


voice = form.file_uploader(
    "Upload a :red[30-60s] sample of your voice to be used as voiceover for the script (optional)",
    type=["wav"],
)
voice_name = form.text_input(
    "Enter your name for the voiceover (optional)", placeholder="John-Doe, etc..."
)
form.markdown(
    """
    Note: 
    - if you already have a clone of your voice, just pass the name of the voice in the field above.
    - if you don't upload a sample of your voice with a name, the script will be generated with an AI Voice.
    - if your file is not in .wav format, you can use this [online converter](https://convertio.co/) to convert it.
"""
)


if form.form_submit_button("Generate"):
    if str.strip(title) == "" or str.strip(description) == "" or str.strip(tone) == "":
        st.error("Please fill the required fields")
        st.stop()
    if voice and not check_audio_length(voice):
        st.error("Please upload a sample of your voice between 30 and 60 seconds")
        st.stop()

    if voice and not voice_name:
        st.error("Please enter your name")
        st.stop()

    if (
        voice_name
        and not voice
        and not check_cloned_voice(str.strip(voice_name).replace(" ", "-"))
    ):
        st.error("Please enter a valid name (the name you used to clone your voice)")
        st.stop()

    if (
        voice
        and voice_name
        and check_cloned_voice(str.strip(voice_name).replace(" ", "-"))
    ):
        st.error(
            "The voice clone already exists, use the name only or upload a new sample and a name to clone a new voice"
        )
        st.stop()

    prompt = (
        f"I want you to act as a scriptwriter for a short YouTube video titled '{title}'. "
        f"Your task is to write a script between 20 and 50 words in a {tone} tone, "
        f"in this format: title then section name then the content of the section. don't write 'content:' for the content of each section. "
        f"dont use special characters, for example dont write '#3' write 'number 3'. "
        f"Consider the video's description: '{description}'. "
        f"{'and the following search terms: {search_term}.' if str.strip(search_term) != '' else ''}"
    )

    with st.spinner("Generating..."):
        script = str.strip(generate(prompt))
        st.divider()
        st.header("📜Script:")
        st.write(script)

        st.divider()

    with st.spinner("Generating..."):
        if voice:
            voice_id = clone_voice(voice, str.strip(voice_name).replace(" ", "-"))
        elif voice_name:
            voice_id = check_cloned_voice(str.strip(voice_name).replace(" ", "-"))
        else:
            voice_id = None

        audio_file = script_to_audio(script.replace("\n\n", ".\n\n"), voice_id)
        st.header("🎧Audio:")
        st.audio(audio_file, format="audio/mp3")
