.. _tutorial_1:

Step 1: Setting up the environment
================================

To get started, we need the KnowledgeNet framework to be installed.

..  attention::
    TODO Recommend virtual environment (conda)

.. code-block:: bash

   $ pip install knowledgenet

Currently, the framework uses OpenAI language models, so we will also need an OpenAI API key. Put it in a file named
:code:`credentials.py`. The credentials file should look like the line below, with your API key replacing "XXX".

.. code-block:: python

    openai_api_key = XXX


