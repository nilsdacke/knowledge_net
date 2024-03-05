from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


system_template = """Use the following quotes to answer the user's question. 
Phrase the answer as straightforward assertions, don't say "the quotes suggest...", don't hedge, don't moralize. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

----------------
{context}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
COMBINE_DOCUMENTS_CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
