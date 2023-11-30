.. _tutorial_2:

Step 2: simple knowledge bases
================================

..  attention::
    TODO make example data and scripts available to the user

Let's create our first conversational knowledge base! The process for doing this starts with preparing text documents
containing the knowledge we want to share and storing chunks of the documents into a vector database.

The KnowledgeNet framework comes with example documents that we can use. The texts are books by nineteenth century
scientists Charles Darwin, Francis Galton and Charles Babbage, from Project Gutenberg. We have
removed the front and back matter from the books, keeping only the main text.

To create a vector data base with computer pioneer Charles Babbage's writings, run the following command:

..  attention::
    TODO script; explain parameters

.. code-block:: bash

   $

To make the knowledge base available to the world, run

.. code-block:: bash

   $

Our Charles Babbage knowledge base is now served over HTTP! How do we talk to it? Run this:

.. code-block:: bash

   $

A chat page should appear in your browser. We can now have a conversation about Babbage's books. Try for example,
"Tell me about the analytical engine."

We will soon take a peek under the hood to better understand what we did. But first, let's create and launch two
additional knowledge bases, about Charles Darwin and Francis Galton.

.. code-block:: bash

   $
