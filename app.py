import streamlit as st
from assistant.processor_setup import setup_query_processor
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

st.set_page_config('ChickenAI',initial_sidebar_state='collapsed')

@st.cache_resource
def get_processor():
    return setup_query_processor(chat_model='llama-3.1-70b-versatile')

st.title("🐔⚙️ Chicken-AI")
st.caption("🚀 A Streamlit chatbot powered by GroqCloud and The Blue Alliance")

with st.sidebar:
    with st.expander("ℹ️ More Info"):
        st.write("""
        Chicken-AI is a chatbot that can answer questions about FIRST Robotics. It uses the GroqCloud API for natural language processing and the The Blue Alliance API for information retrieval.
                 
        As of know, ChickenAI can be used to answer the following queries:
        - What is the team number for team <team_name>?
        - Give me some information about team <team_name/team_number>.
            - School affiliation
            - Location
            - Rookie year
        - What events did <team_name/team_number> attend during the <year> season?
        - What events are happening in <state_name> during the <year> season?
        - What awards did <team_name/team_number> win during the <year> season?
        - What are the highest ranked teams in <district_name> during the <year> season?
                 
        These are just some sample questions, feel free to ask anything you want!
        """)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar":"🐔", "content": "How can I help you?"}]

for msg in st.session_state.messages:

    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🐔").write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🐔").write(prompt)

    with st.spinner("Thinking..."):
        msg = get_processor().generate_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant", avatar="🤖").write(msg)