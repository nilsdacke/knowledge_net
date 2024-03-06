import sys
from pathlib import Path

from langchain_openai import ChatOpenAI

from knowledge_net.comm_shell.comm_shell_http import Server
from knowledge_net.langchain.rag_knowledgebase import LangchainRAGKnowledgebase
from credentials import openai_api_key


if len(sys.argv) != 6:
    print("Usage: python http_server_rag.py <knowledgebase identifier> <display name> <database directory> "
          "<source info file> <port>")
    sys.exit()

kb_name = sys.argv[1]
display_name = sys.argv[2]
database_location = Path(sys.argv[3])
source_descriptions_file = Path(sys.argv[4])
port = int(sys.argv[5])

LLM_DEFAULT_MODEL = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=LLM_DEFAULT_MODEL, temperature=0, openai_api_key=openai_api_key)
LangchainRAGKnowledgebase(database_location=database_location,
                          source_descriptions_file=source_descriptions_file,
                          identifier=kb_name,
                          openai_api_key=openai_api_key,
                          llm=llm,
                          display_name=display_name).share()

Server.serve(port=port)
