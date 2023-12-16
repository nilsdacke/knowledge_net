.. _tutorial_3b:

Step 3, continued
================================

Some explanations of what we just did:

* The knowledge bases to instantiate are described in the JSON files in :code:`examples/knowledgebases/victorian`
* A local knowledge base of class :code:`RoutingKnowledgebase` is instantiated
* The routing knowledge base connects to the remote knowledge bases :code:`babbage`, :code:`darwin` and :code:`galton`
* The routing knowledge base uses the descriptions of the remote knowledge bases to match them to queries
* A knowledge base named :code:`general` is used to catch queries not matching any specialist knowledge base
* Our :code:`general` knowledge base simply replies that it doesn't know; this could be replaced with more capable behavior



