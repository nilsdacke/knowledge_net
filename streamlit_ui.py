import streamlit as st
# import random

from knowledge_net.chat.chat_event import MessageEvent
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

st.title("The KnowledgeNet begins...")

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatHistory()
    st.session_state.kb = Knowledgebase(preferred_protocol='mock')

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
    st.session_state.chat_history.extend(response)
