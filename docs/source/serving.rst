.. _serving:

Serving a knowledge base
================================

Let's assume you have already created a knowledge base, implemented by the class :code:`MyKnowledgebase`, and want to
share it with the world. Easy:

.. code-block:: python

    from knowledge_net.comm_shell.comm_shell_http import Server
    from my_knowledge.knowledgebase.my_knowledgebase import MyKnowledgebase

    PORT = 8001
    MyKnowledgebase().share()

    Server.serve(port=PORT)

Just instantiate your knowledge base and invoke the HTTP server provided by the framework. In the next section we will
learn how to implement a knowledge base.