import streamlit as st
import time
import numpy as np
from helper import load_youtube_video, answer_question


if 'youtube_video_docs' not in st.session_state:
    st.session_state.youtube_video_docs = None

if 'youtube_video_summary' not in st.session_state:
    st.session_state.youtube_video_summary = None

if "youtube_video_messages" not in st.session_state:
    st.session_state.youtube_video_messages = []


def stream_data(res):
    for word in res.split(" "):
        yield word + " "
        time.sleep(0.02)


st.write("# Summarize Youtube Videos.")

form = st.form("my_form")
youtube_video_link = form.text_input("Enter Youtube Video Link", "", placeholder="Enter Youtube Video Link")
submitted = form.form_submit_button('Summarize')

if submitted:
    try:
        st.video(youtube_video_link)
    except:
        st.error("Unable to load video :cry:")

    try:
        (response, docs) = load_youtube_video(youtube_video_link)
        st.session_state.youtube_video_summary = response
        st.session_state.youtube_video_docs = docs
        st.session_state.youtube_video_messages = []
    except:
        st.error("Oops! Unable to summarize video :sob:")


if st.session_state.youtube_video_summary:
    st.write("###")
    st.header("_Summary_", divider='violet')
    st.write(st.session_state.youtube_video_summary)

    st.write("###")
    st.header("_Any Doubt? Clear it._", divider='violet')
    # Display chat messages from history on app rerun
    for message in st.session_state.youtube_video_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Any Doubt? Clear it."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.youtube_video_messages.append({"role": "user", "content": prompt})

        response = answer_question(st.session_state.youtube_video_docs, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.youtube_video_messages.append({"role": "assistant", "content": response})
