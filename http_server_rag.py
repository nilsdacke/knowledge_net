import sys
from pathlib import Path

from knowledge_net.comm_shell.comm_shell_http import Server
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

from knowledge_net.experimental.rag_knowledgebase.rag_knowledgebase import RAGKnowledgebase
from credentials import openai_api_key


port: int = 8001

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python http_server.py <knowledgebase identifier> [<port>]")
    sys.exit()
elif len(sys.argv) == 3:
    port = int(sys.argv[2])

kb_name = sys.argv[1]

if kb_name == "victorian-science":
    display_name = "Victorian Science"
    database_location = Path("db/victorian-science")
elif kb_name == "galton":
    display_name = "Francis Galton"
    database_location = Path("db/galton")
elif kb_name == "darwin":
    display_name = "Charles Darwin"
    database_location = Path("db/darwin")
elif kb_name == "babbage":
    display_name = "Charles Babbage"
    database_location = Path("db/babbage")
else:
    raise ValueError(f"Unknown knowledge base {kb_name}")

source_descriptions_file = Path("meta/source_info.json")
Knowledgebase.share(RAGKnowledgebase(database_location=database_location,
                                     source_descriptions_file=source_descriptions_file,
                                     identifier=kb_name,
                                     openai_api_key=openai_api_key,
                                     display_name=display_name))

Server.serve(port=port)
