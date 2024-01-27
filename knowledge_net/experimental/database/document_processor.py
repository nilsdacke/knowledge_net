from abc import ABC, abstractmethod
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain.schema import Document

from knowledge_net.experimental.database.sentence_splitter import SentenceTextSplitter


class DocumentProcessor(ABC):
    """Converts a file into embeddable chunks."""

    DEFAULT_SPLITTER = SentenceTextSplitter(
        chunk_size=1200,
        chunk_overlap=400,
        add_start_index=True
    )

    def __init__(self):
        self.splitter = DocumentProcessor.DEFAULT_SPLITTER

    def __call__(self, file: Path) -> list[Document]:
        """Applies the processor to the file."""
        return self.prepare(file)

    def prepare(self, file: Path) -> list[Document]:
        """Converts the file into chunks."""
        docs = self.collect_text(file)
        docs = self.prepare_text(docs)
        docs = self.split(docs)
        return docs

    def prepare_for_file(self, file: Path) -> str:
        """Processes file without chunking, suitable for file output."""
        docs: list[Document] = self.collect_text(file)
        docs = self.prepare_text(docs)
        return '\n'.join([d.page_content for d in docs])

    @abstractmethod
    def collect_text(self, file: Path) -> list[Document]:
        """Converts the file into text document objects. Must be implemented by a subclass."""
        pass

    def prepare_text(self, docs: list[Document]) -> list[Document]:
        """Edits the text in any way necessary. By default, does nothing."""
        return docs

    def split(self, docs: list[Document]) -> list[Document]:
        """Splits the text into embeddable chunks."""
        return self.splitter.split_documents(docs)


class TextDocumentProcessor(DocumentProcessor):
    """Converts a plain text document into embeddable chunks."""

    def collect_text(self, file: Path) -> list[Document]:
        """Loads text from a plain text file."""
        return TextLoader(str(file)).load()
