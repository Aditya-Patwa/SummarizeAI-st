import streamlit as st
from helper import load_web_page, answer_question
import time
import numpy as np
import pandas as pd

if 'webpage_docs' not in st.session_state:
    st.session_state.webpage_docs = None

if 'webpage_summary' not in st.session_state:
    st.session_state.webpage_summary = None

if "webpage_messages" not in st.session_state:
    st.session_state.webpage_messages = []

st.header("Summarize Webpage.")

form = st.form("my_form")
webpage_link = form.text_input("Enter Webpage Link", "", placeholder="Enter Webpage Link")
submitted = form.form_submit_button("Summarize")

def stream_data(res):
    for word in res.split(" "):
        yield word + " "
        time.sleep(0.02)

if submitted:
    try: 
        (response, docs) = load_web_page(webpage_link)
        st.session_state.webpage_summary = response
        st.session_state.webpage_docs = docs
        st.session_state.webpage_messages = []
    except:
        st.error("Oops! Unable to summarize webpage. :sob:")


if st.session_state.webpage_summary:
    st.write("###")
    st.header("_Summary_", divider='violet')
    st.write(st.session_state.webpage_summary)

    st.write("###")
    st.header("_Ask Doubt? Clear it._", divider='violet')
    # Display chat messages from history on app rerun
    for message in st.session_state.webpage_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Doubt? Clear it."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.webpage_messages.append({"role": "user", "content": prompt})

        response = answer_question(st.session_state.webpage_docs, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.webpage_messages.append({"role": "assistant", "content": response})