.. _overview:

The KnowledgeNet framework
================

The KnowledgeNet is a decentralized network of conversational knowledge bases. The KnowledgeNet framework supports its
implementation. The framework

* Helps you create knowledge bases
* Facilitates the communication between knowledge bases

The framework architecture has two layers: the knowledge kernel and the communication shell. You will find the code for
the communication shell in the `comm_shell` directory. It currently supports HTTP and makes it straightforward to
implement other communication protocols.

The knowledge kernel is implemented in the other source directories. The main classes are:

* `Knowledgebase`
* `ChatHistory`

A `Knowledgebase` can be a local knowledge base running in the process of your program or a remote knowledge base
accessed for example over HTTP. The `ChatHistory` records the interactions between the user and the knowledge bases.

