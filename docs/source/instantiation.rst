.. _instantiation:

More on knowledge base instantiation
======================================

So far, we have instantiated knowledge bases directly in our code. If you have many knowledge bases or want to change
the set of knowledge bases dynamically, a better way is to instantiate them from json files.

The default file structure for this looks like this:

::

    <my_project>
        knowledgebases
            top_level.json
            <my_knowledgebase>.json
            <my_other_knowledgebase>.json

The file top_level.json specifies the knowledge bases that you want to share publicly. For each local knowledge base
that you instantiate, there is also a file named :code:`<knowledgebase_identifier>.json`. It specifies the list of knowledge
bases that the local knowledge base will talk to.

All the files have the same structure. Each file contains a list of dictionaries, each of which specifies a knowledge
base. For a remote knowledge base, it specifies how to connect. For a local one, it provides the module, class, and
parameters (:code:`kwargs`) needed to instantiate it.

.. code-block:: json

    [
        {
            "identifier": "ama",
            "display_name": "Ask me anything :-)",
            "protocol": "local",
            "protocol_details": {
                "module": "ama.knowledgebase.knowledgebase_ama",
                "class": "KnowledgebaseAMA",
                "kwargs": {}
            }
        },
        {
            "identifier": "galton",
            "display_name": "The world of Francis Galton",
            "protocol": "http",
            "protocol_details": {
                "url": "http://localhost:8001"
            }
        }
    ]

To instantiate the listed knowledge bases, call the static method :code:`Knowledgebase.load`.