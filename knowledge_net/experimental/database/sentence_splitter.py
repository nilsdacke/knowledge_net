import re
from typing import Any
from langchain.text_splitter import TextSplitter


class SentenceTextSplitter(TextSplitter):
    """Splits text along sentence boundaries."""

    SPLIT_PATTERN = "[.?!]|\n\n"

    def __init__(self,
                 chunk_size: int = 1200,
                 chunk_overlap: int = 400,
                 add_start_index: bool = True,
                 **kwargs: Any):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index,
                         keep_separator=True, **kwargs)

    def split_text(self, text: str) -> list[str]:
        first_splits = self.split_on_pattern(text)
        sentences = self.append_separators(first_splits)
        return self._merge_splits(sentences, separator="")

    def split_on_pattern(self, text: str) -> list[str]:
        return [s for s in re.split(f"({self.SPLIT_PATTERN})", text) if s]

    def append_separators(self, splits: list[str]) -> list[str]:
        concatenated = []
        for s in splits:
            if concatenated and re.fullmatch(self.SPLIT_PATTERN, s):
                concatenated[-1] += s
            else:
                concatenated.append(s)
        return concatenated


