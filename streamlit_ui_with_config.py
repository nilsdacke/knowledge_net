import sys
from pathlib import Path

import streamlit as st
from knowledge_net.chat.chat_event import MessageEvent
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
from credentials import openai_api_key


configuration_directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("knowledgebases-galton-gpt")

st.title("Ask me anything...")

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatHistory()

if "kb" not in st.session_state:
    Knowledgebase.keys["openai_api_key"] = openai_api_key
    Knowledgebase.instantiate_public(configuration_directory)
    st.session_state.kb = Knowledgebase.single_public_instance()

for message in st.session_state.chat_history.get_messages():
    with st.chat_message(message.role):
        st.markdown(message.message_text)

if prompt := st.chat_input("What do you want to learn about?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append(MessageEvent(message_text=prompt))
    response = st.session_state.kb.reply(st.session_state.chat_history)
    for message in response.get_messages():
        with st.chat_message(message.role):
            st.markdown(message.message_text)
    if response.returned_error():
        called, error = response.get_error()
        with st.chat_message("assistant"):
            st.markdown(f"Knowledge base {called} error: \"{error}\"")
    st.session_state.chat_history.extend(response)
