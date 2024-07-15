import streamlit as st
import time
import numpy as np


st.write("# Summarize Youtube Videos.")

youtube_video_link = st.text_input("Enter Youtube Video Link", "", placeholder="Enter Youtube Video Link")


if youtube_video_link:
    try:
        st.video(youtube_video_link)
    except:
        st.error("Unable to load video :cry:")

    try:
        prompt = st.text_input("Ask Doubt? Clear it.", placeholder="Ask any question related to video.")

        if prompt:
            st.write(f"Question: {prompt}")
    except:
        st.error("Oops! Unable to summarize video :sob:")

