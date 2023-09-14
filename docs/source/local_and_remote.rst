.. _local_remote:

Local and remote knowledge bases
====================================

We have so far discussed local knowledge bases that run in the same process on your machine. There are also remote
knowledge bases that are accessed over a communication protocol such as HTTP.

Below we instantiate a remote knowledge base.

.. code-block:: python

    remote_knowledgebase = Knowledgebase(
        identifier="history_kb",
        display_name="World of history",
        protocol="http",
        protocol_details={
            "url": "my_knowledgebase.net"
        },
        make_public=False
    )

We can now call this knowledge base exactly like you would a local one, using its :code:`reply` method.