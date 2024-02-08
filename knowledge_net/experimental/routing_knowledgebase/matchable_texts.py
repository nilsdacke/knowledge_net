from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document


class MatchableTexts:
    """Supports similarity search on a collection of texts.

    The class is useful when implementing routing where you need to pick one or more knowledge bases with descriptions
    matching a query.
    """

    collection_id: int = 0

    def __init__(self, named_texts: dict[str, str], openai_api_key: str):
        documents = [Document(page_content=t, metadata={"name": n}) for n, t in named_texts.items()]
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        unique_name = f"Collection_{MatchableTexts.collection_id}"
        self.vector_store = Chroma.from_documents(documents, embeddings, collection_name=unique_name)
        MatchableTexts.collection_id += 1

    def search_with_score(self, query: str, k: int = 1) -> list[tuple[str, float]]:
        """Returns the names and scores of the top k matching texts."""
        return [(d.metadata['name'], s) for d, s in
                self.vector_store.similarity_search_with_score(query, k=k)]

    def best(self, query: str, k: int = 1) -> list[str]:
        """Returns the names of the top k matching texts."""
        # Uncomment to print scores for each item
        # with_scores = self.vector_store.similarity_search_with_score(query, k=k)
        # print([f"{d.metadata['name']} score = {s}" for d, s in with_scores])
        return [d.metadata['name'] for d in self.vector_store.similarity_search(query, k=k)]

    def better_than(self, query: str, baseline_name: str = "general", k: int = 3) -> list[str]:
        """Returns the names of the texts scoring better than the baseline up to a maximum of k texts."""
        names = self.best(query, k=k)
        baseline_index = names.index(baseline_name) if baseline_name in names else k
        return names[:baseline_index]

    def better_than_or_equal(self, query: str, baseline_name: str = "general", k: int = 3) -> list[str]:
        """Returns the names of the texts scoring >= the baseline up to a maximum of k texts."""
        names = self.best(query, k=k)
        baseline_index = names.index(baseline_name) if baseline_name in names else k
        return names[:baseline_index + 1]

    def baseline_or_better(self, query: str, baseline: str = "general", k: int = 3) -> list[str]:
        """Returns the names of the texts scoring better than the baseline, or baseline if none is better, max k."""
        better = self.better_than(query, baseline, k=k)
        return better or [baseline]
