import sys
from pathlib import Path

from knowledge_net.comm_shell.comm_shell_http import Server
from credentials import openai_api_key
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

if len(sys.argv) != 3:
    print("Usage: python http_server_with_config.py <config directory> <port>")
    sys.exit()

configuration_directory = Path(sys.argv[1])
port = int(sys.argv[2])

Knowledgebase.keys["openai_api_key"] = openai_api_key
Knowledgebase.instantiate_public(configuration_directory)

Server.serve(port=port)
