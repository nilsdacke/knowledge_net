.. _chat_history:

Chat history
======================================

The :code:`ChatHistory` records the interactions between the user and the knowledge bases. Knowledge bases communicate
by passing :code:`ChatHistory` objects.

The data structure resembles the chat
history used with chat language models, but has a few extensions. The history contains not only messages but also
conversation summaries and other events, like errors and calls to and returns from connected knowledge bases.
The latter kinds are added automatically by the framework. 

A :code:`ChatHistory` representing the conversation so far is passed as an argument to
:code:`Knowledgebase._reply`. Your implementation of this method will return another :code:`ChatHistory` instance
that contains the continuation of the chat.

.. code-block:: python

    class MyKnowledgebase(Knowledgebase):
        ...

        def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
            messages_so_far = chat_history.get_messages()  # Ignore conversation so far
            new_messages = [self.message("Hello world!"), self.message("Have a nice day.")]  # Make new messages
            chat_continuation = ChatHistory(new_messages)
            error = None
            return chat_continuation, error