import streamlit as st


home = st.Page("home.py", title="Home", icon=":material/home:")
summarize_youtube_video = st.Page("summarize_youtube_video.py", title="Summarize Youtube Video", icon=":material/youtube_activity:")
summarize_web_page = st.Page("summarize_web_page.py", title="Summarize Webpage.", icon=":material/globe:")

pg = st.navigation({
    "Home": [home],
    "Products": [summarize_web_page, summarize_youtube_video],
})

st.set_page_config(page_title="SummarizeAI - TLDR; made easy with SummarizeAI. Get summaries in a flash!⚡️", page_icon="📖")

st.header('SummarizeAI', divider='rainbow')
pg.run()

