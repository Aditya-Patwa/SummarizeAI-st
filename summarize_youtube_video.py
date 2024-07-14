import streamlit as st
import time
import numpy as np

st.write("# Summarize Youtube Videos.")

youtube_video_link = st.text_input("Enter Youtube Video Link", "https://www.youtube.com/watch?v=YmAaKKlDy7k", placeholder="Enter Youtube Video Link")


try:
    st.video(youtube_video_link)
except:
    st.error("Unable to load video")





prompt = st.text_input("Ask Doubt? Clear it.", placeholder="Ask any question related to video.")

if prompt:
    st.write(f"Question: {prompt}")

