.. _calling:

Calling knowledge bases
======================================

Knowledge bases can talk to each other. You call another knowledge base by invoking its :code:`reply` method.

.. code-block:: python

    response = other_knowledgebase.reply(chat_history, caller=self.identifier)





