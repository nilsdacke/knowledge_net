.. _protocols:

Communication protocols
========================

The KnowledgeNet framework currently only supports communication over HTTP, but it can be extended to other
protocol such as HTTPS and NOSTR. To add a new protocol to the framework,

1. Create a new file named comm_shell_<my_protocol>.py inside the comm_shell directory
2. In this file, add a class named CommShell<My_protocol>, like CommShellHttp
3. Implement the :code:`reply` method

The interface of the method is shown below.

.. code-block:: python

    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol_details: Any) -> Tuple[ChatHistory, Optional[str]]:

Now, if you instantiate a knowledge base with :code:`protocol=<my_protocol>`, calls to it will be automatically dispatched
through your protocol.