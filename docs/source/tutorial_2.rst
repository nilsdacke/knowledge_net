.. _tutorial_2:

Step 2: Simple knowledge bases
================================

..  attention::
    TODO make example data and scripts available to the user

Let's create our first conversational knowledge base! The process for doing this starts with preparing text documents
containing the knowledge we want to share and storing chunks of the documents into a vector database.

The KnowledgeNet framework comes with example documents that we can use. The texts are books by nineteenth century
scientists Charles Darwin, Francis Galton and Charles Babbage, from Project Gutenberg. We have
removed the front and back matter from the books, keeping only the main text.

To create a vector data base with computer pioneer Charles Babbage's writings, run the following command:

.. code-block:: bash

   $ python build_database.py examples/documents/babbage/ db/babbage

To make the knowledge base available to the world, run

.. code-block:: bash

   $ python http_server_rag.py babbage "Charles Babbage" db/babbage examples/meta/victorian_science_sources.json 8001&

Our Charles Babbage knowledge base is now served over HTTP! How do we talk to it? Run this:

.. code-block:: bash

   $ streamlit run streamlit_ui.py -- babbage http://localhost:8001

A chat page should appear in your browser. We can now have a conversation about Babbage's life and work.
Try for example, "Tell me about the analytical engine."

We will soon take a peek under the hood to better understand what we did. But first, let's create and launch two
additional knowledge bases, about Charles Darwin and Francis Galton.

.. code-block:: bash

   $ python build_database.py examples/documents/darwin/ db/darwin
   $ python build_database.py examples/documents/galton/ db/galton

