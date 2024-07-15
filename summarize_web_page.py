import streamlit as st
from helper import load_web_page
import time
import numpy as np
import pandas as pd

st.header("Summarize Webpage.")

webpage_link = st.text_input("Enter Webpage Link", "", placeholder="Enter Webpage Link")


def stream_data(res):
    for word in res.split(" "):
        yield word + " "
        time.sleep(0.02)

if webpage_link:
    try: 
        response = load_web_page(webpage_link)
        st.write("###")
        st.header("_Summary_", divider='violet')
        st.write_stream(stream_data(response))
    except:
        st.error("Oops! Unable to summarize webpage. :sob:")