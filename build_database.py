import sys
from pathlib import Path

from knowledge_net.experimental.database.database import Database
from knowledge_net.experimental.database.document_processor import TextDocumentProcessor
from credentials import openai_api_key

if len(sys.argv) != 2:
    print("Usage: python build_database.py <knowledgebase name>")
    sys.exit()

knowledgebase_name = sys.argv[1]

processor = TextDocumentProcessor()
document_path = Path(f"examples/documents/{knowledgebase_name}")
database_path = Path(f"db/{knowledgebase_name}")

Database(database_path, openai_api_key=openai_api_key).build_from_folder(document_path, processor)
