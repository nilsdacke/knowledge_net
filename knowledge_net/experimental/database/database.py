import os.path
import shutil
from pathlib import Path

from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from knowledge_net.experimental.database.document_pipeline import DocumentPipeline
from knowledge_net.experimental.database.document_processor import DocumentProcessor


class Database:
    """Creates and loads the vector database."""

    def __init__(self, directory: Path, openai_api_key: str):
        self.directory = directory
        self.openai_api_key = openai_api_key

    def build_from_folder(self, document_directory: Path, processor: DocumentProcessor) -> Chroma:
        """Convenience function that builds a database from all the files in a folder and sub folders."""
        pipeline = DocumentPipeline()
        pipeline.add_recursively(document_directory, processor)
        docs = pipeline.prepare_all()
        return self.build(docs)

    def build(self, docs: list[Document]) -> Chroma:
        """Builds a Chroma database from the documents.

        If the database directory exists, it will be deleted before creating the new database.
        """

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
        database = Chroma.from_documents(
            documents=docs,
            embedding=self.get_embeddings(),
            persist_directory=str(self.directory)
        )
        database.persist()
        return database

    def load(self) -> Chroma:
        """Loads the database from the persistent directory."""
        return Chroma(embedding_function=self.get_embeddings(), persist_directory=str(self.directory))

    def get_embeddings(self) -> OpenAIEmbeddings:
        """Returns the embeddings to use."""
        return OpenAIEmbeddings(openai_api_key=self.openai_api_key)
