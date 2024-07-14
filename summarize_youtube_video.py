import streamlit as st
import time
import numpy as np
from langchain_huggingface import HuggingFaceEndpoint
from langchain.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)



st.write("# Summarize Youtube Videos.")

youtube_video_link = st.text_input("Enter Youtube Video Link", "", placeholder="Enter Youtube Video Link")


if youtube_video_link:
    try:
        st.video(youtube_video_link)
    except:
        st.error("Unable to load video :cry:")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(YoutubeLoader.extract_video_id(youtube_video_link))
        loader = YoutubeLoader.from_youtube_url(youtube_video_link,
            add_video_info=True,
            language=["en", next(iter(transcript_list)).language_code],
            translation="en")
        transcript = loader.load()
        prompt = st.text_input("Ask Doubt? Clear it.", placeholder="Ask any question related to video.")

        if prompt:
            st.write(f"Question: {prompt}")
    except:
        st.error("Oops! Unable to summarize video :sob:")

