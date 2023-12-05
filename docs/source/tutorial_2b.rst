.. _tutorial_2b:

Step 2, continued
================================

..  attention::
    TODO provide code snippets

Let us take a look into the KnowledgeNet source code to understand what we just did. Creating a vector database
requires the following steps.

#. Preparing text documents containing the knowledge we want to share
#. Splitting the texts into chunks
#. Converting the chunks into embeddings (vectors)
#. Storing the embeddings in a vector database

The :code:`build_database.py` script performs steps 2-4, using OpenAI embeddings and the Chroma vector database.

The :code:`http_server_rag.py` script instantiates a conversational knowledge base and serves it over HTTP.
The script uses the
class :code:`RAGKnowledgebase`, provided by the framework. Custom knowledge bases can be created by subclassing the
:code:`Knowledgebase` base class.

The :code:`streamlit_ui.py` script connects to our knowledge base and presents us with a chat user interface.

