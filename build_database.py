import sys
from pathlib import Path

from knowledge_net.experimental.database.database import Database
from knowledge_net.experimental.database.document_processor import TextDocumentProcessor
from credentials import openai_api_key

if len(sys.argv) != 3:
    print("Usage: python build_database.py <document directory> <db directory>")
    sys.exit()

document_path = Path(sys.argv[1])
database_path = Path(sys.argv[2])

processor = TextDocumentProcessor()
Database(database_path, openai_api_key=openai_api_key).build_from_folder(document_path, processor)
