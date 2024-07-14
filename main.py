import streamlit as st


home = st.Page("home.py", title="Home", icon=":material/home:")
summarize_youtube_video = st.Page("summarize_youtube_video.py", title="Summarize Youtube Video", icon=":material/youtube_activity:")

pg = st.navigation({
    "Home": [home],
    "Products": [summarize_youtube_video],
})

st.set_page_config(page_title="Home", page_icon=":material/home:")

st.header('SummarizeAI', divider='rainbow')
pg.run()

