import sys
from pathlib import Path

from knowledge_net.comm_shell.comm_shell_http import Server
from knowledge_net.experimental.rag_knowledgebase.rag_knowledgebase import RAGKnowledgebase
from credentials import openai_api_key


if len(sys.argv) != 6:
    print("Usage: python http_server.py <knowledgebase identifier> <display name> <database directory> "
          "<source info file> <port>")
    sys.exit()

kb_name = sys.argv[1]
display_name = sys.argv[2]
database_location = Path(sys.argv[3])
source_descriptions_file = Path(sys.argv[4])
port = int(sys.argv[5])

RAGKnowledgebase(database_location=database_location,
                 source_descriptions_file=source_descriptions_file,
                 identifier=kb_name,
                 openai_api_key=openai_api_key,
                 display_name=display_name).share()

Server.serve(port=port)
