.. _knowledgebase:

Creating a knowledge base
===========================

To implement a knowledge base, subclass the :code:`Knowledgebase` class and override the method :code:`_reply`.
This method takes a chat history and returns the chat continuation together with an error message (or :code:`None`).

.. code-block:: python

    from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
    from knowledge_net.chat.chat_history import ChatHistory

    class MyKnowledgebase(Knowledgebase):
        def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
            return ChatHistory([self.message("Hello world")]), None