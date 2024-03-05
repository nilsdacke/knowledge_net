from typing import Optional, Any
from langchain.schema import Document


class MetadataGroup:
    """Groups documents with similar metadata."""

    def __init__(self, key: str, value: str, documents: list[Document]):
        """Initializes group of documents where metadata[key] == value."""
        self.key = key
        self.value = value
        self.documents = documents

    def matches(self, document: Document) -> bool:
        """True if the document should be included in the group."""
        return self.value == self.document_value(document)

    def add(self, document: Document):
        """Adds the document to the group."""
        self.documents.append(document)

    def document_value(self, document: Document):
        """Gets the value of the document as defined by the group."""
        return self.document_value_from_key(document, self.key)

    def to_string(self) -> str:
        """Turns the group into a single string."""
        return "\n\n".join([f'"{d.page_content}"' for d in self.documents])

    def to_document_with_description(self, descriptions: dict[str, dict[str, str]]) -> Document:
        """Turns the group into a document with a description drawn directly from the `descriptions`.

        The structure of the dictionary is from key to value to description.
        Metadata are discarded.
        """
        content = "\n\n".join([self.get_from_dictionary(descriptions), self.to_string()])
        return Document(page_content=content)

    def to_document_with_book_intro(self, descriptions: dict[str, dict[str, dict[str, str]]]) -> Document:
        """Turns the group into a document with an introduction built from the `descriptions`.

        Convenience function for when the common key is 'source' (or similar) and we introduce a book.
        Produces a line like: "In Noteworthy Families, from 1906, Francis Galton writes:"

        The structure of the dictionary is from key to value to description.
        Metadata are discarded.
        """
        attributes = self.get_from_dictionary(descriptions)
        if attributes and 'title' in attributes and 'author' in attributes:
            year = f"from {attributes['year']}, " if 'year' in attributes else ""
            intro = f"In {attributes['title']}, {year}{attributes['author']} writes:"
            content = "\n\n".join([intro, self.to_string()])
        else:
            content = ""
        return Document(page_content=content)

    def get_from_dictionary(self, dictionary: dict[str, dict[str, Any]]) -> Any:
        """Retrieves a dictionary value corresponding to the group's key and value."""
        return dictionary[self.key][self.value] if self.key in dictionary and self.value in dictionary[self.key] else ""

    @staticmethod
    def document_value_from_key(document: Document, key: str):
        """Gets the value of the document as defined by the key."""
        return document.metadata[key] if key in document.metadata else None

    @staticmethod
    def group_documents_by_key(documents: list[Document], key: str) -> list["MetadataGroup"]:
        """Creates list of groups, each containing documents with equal values for metadata[key]."""
        groups: list[MetadataGroup] = []
        for d in documents:
            matching_group: Optional[MetadataGroup] = MetadataGroup.find_matching_group(d, groups)
            if matching_group:
                matching_group.add(d)
            else:
                value = MetadataGroup.document_value_from_key(d, key)
                new_group = MetadataGroup(key=key, value=value, documents=[d])
                groups.append(new_group)

        return groups

    @staticmethod
    def find_matching_group(document: Document, groups: list["MetadataGroup"]):
        """From a list of groups, return the first group matching the document."""
        matching_group: Optional[MetadataGroup] = None
        for g in groups:
            if g.matches(document):
                matching_group = g
                break
        return matching_group
