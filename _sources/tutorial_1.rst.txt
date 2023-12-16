.. _tutorial_1:

Step 1: Setting up the environment
================================

To get started, we need the KnowledgeNet framework to be installed.

.. code-block:: bash

   $ git clone https://github.com/nilsdacke/knowledge_net.git

To install prerequisite libraries, it is best to create a virtual environment. The Python version should be >=3.9.
With Anaconda:

.. code-block:: bash

   $ conda create -n knowledge_net python=3.10
   $ conda activate knowledge_net

Install required libraries:

.. code-block:: bash

   $ pip install -r requirements.txt

Currently, the framework uses OpenAI language models, so we will also need an OpenAI API key. Put it in a file named
:code:`credentials.py` in the top-level :code:`knowledge_net` directory.
The credentials file should look like the line below, with your API key replacing "XXX".

.. code-block:: python

    openai_api_key = "XXX"


