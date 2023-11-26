import os
from pathlib import Path
from typing import Optional

from langchain.schema import Document
from knowledge_net.experimental.database.document_processor import DocumentProcessor, TextDocumentProcessor


class DocumentPipeline:
    """Converts documents (files) to embeddable chunks."""

    def __init__(self):
        self.files: list[tuple[Path, Optional[DocumentProcessor]]] = []
        self.default_processors: dict[str, DocumentProcessor] = {
            "txt": TextDocumentProcessor()
        }

    def add_file(self, file: Path, document_processor: Optional[DocumentProcessor] = None):
        """Adds a single file to the files to process."""
        self.files.append((file, document_processor))

    def add_from_folder(self, folder: Path, document_processor: Optional[DocumentProcessor] = None):
        """Adds the contents of the folder to the files to process."""
        self.files.extend([(f, document_processor) for f in folder.iterdir() if not f.name.startswith('.')])

    def add_recursively(self, folder: Path, document_processor: Optional[DocumentProcessor] = None):
        """Adds the contents of a folder and its sub folders to the files to process."""
        for path in folder.iterdir():
            if not path.name.startswith('.'):
                if path.is_dir():
                    self.add_recursively(path, document_processor)
                else:
                    self.add_file(path, document_processor)

    def prepare_all(self) -> list[Document]:
        """Turns all the files into embeddable chunks."""
        return [d for docs in [self.prepare_one(f, p) for (f, p) in self.files] for d in docs]

    def prepare_one(self, file: Path, processor: DocumentProcessor) -> list[Document]:
        """Turns a single file into embeddable chunks."""
        processor = processor or self.get_default_processor(file)
        return processor(file)

    @staticmethod
    def sure_directories(file_path: Path):
        """Creates parent directories if they don't exist."""
        os.makedirs(file_path.parent, exist_ok=True)

    def write_one_to_file(self, file: Path, processor: DocumentProcessor, source_root: Path, destination_root: Path):
        """Processes a single file without chunking, writes it to an output file."""

        processor = processor or self.get_default_processor(file)
        output_text = processor.prepare_for_file(file)
        assert str(source_root) in str(file), f"File path {file} does not contain source root {source_root}"
        destination_path = Path(str(file).replace(str(source_root), str(destination_root), 1))
        DocumentPipeline.sure_directories(destination_path)
        with open(destination_path, "w") as f:
            f.write(output_text)

    def write_all_to_files(self, source_root: Path, destination_root: Path):
        """Pre-processes all files without chunking them, writes the results to files.

        Useful for producing documents that can be input to other retrieval systems.
        """
        for (f, p) in self.files:
            self.write_one_to_file(file=f, processor=p, source_root=source_root, destination_root=destination_root)

    @staticmethod
    def convert_folder(input_directory: Path, output_directory: Path, processor: DocumentProcessor):
        """Processes all files under the input_directory and writes the results to the output_directory."""
        pipe = DocumentPipeline()
        pipe.add_recursively(input_directory, processor)
        pipe.write_all_to_files(source_root=input_directory, destination_root=output_directory)

    def get_default_processor(self, file: Path) -> DocumentProcessor:
        """Returns the default document processor for the file, based on its type."""
        suffix = file.suffix
        if suffix == ".crdownload":
            suffix = Path(file.stem).suffix
        return self.default_processors[suffix[1:]]
