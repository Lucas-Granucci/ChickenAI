import streamlit as st

st.title("🐔⚙️ Chicken-AI")
st.caption("🚀 A Streamlit chatbot powered by GroqCloud and The Blue Alliance")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar":"🐔", "content": "How can I help you?"}]

for msg in st.session_state.messages:

    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🐔").write(msg["content"])

def get_query_response(prompt):
    return "This is a test response: " + prompt

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="💬").write(prompt)

    msg = get_query_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant", avatar="🤖").write(msg)