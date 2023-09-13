.. _knowledgebase:

Creating a knowledge base
===========================

To implement a knowledge base, subclass the :code:`Knowledgebase` class and override the method :code:`_reply_local`.
This method takes a chat history and returns the chat continuation together with an error message (or :code:`None`).
You can also override the :code:`Knowledgebase.__init__` method to set an identifier and a display name for the
knowledge base.

.. code-block:: python

    from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
    from knowledge_net.chat.chat_history import ChatHistory

    class MyKnowledgebase(Knowledgebase):
        def __init__(self, make_public: bool = True):
            super().__init__(identifier="my_knowledgebase", display_name="My Knowledgebase", make_public=make_public)

        def _reply_local(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
            return ChatHistory([self.message("Hello world")]), None