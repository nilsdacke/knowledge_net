from langchain.schema import Document
from knowledge_net.experimental.metadata.metadata_group import MetadataGroup


class DocumentGroupTransform:
    """Callable that transforms document lists according to their metadata."""

    def __init__(self, key: str, descriptions: dict[str, dict[str, dict[str, str]]]):
        self.key = key
        self.descriptions = descriptions

    def __call__(self, documents: list[Document]) -> list[Document]:
        groups = MetadataGroup.group_documents_by_key(documents, self.key)
        return [g.to_document_with_book_intro(descriptions=self.descriptions) for g in groups]
