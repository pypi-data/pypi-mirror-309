from typing import List, Union

MAX_LENGTH = 300


class Summarizer:
    def __init__(self, llm: 'LLM'):
        """
        Initialize the Summarizer with an LLM instance.

        Parameters
        ----------
        llm : LLM
            An instance of the LLM class used for generating summaries.
        """
        self.llm = llm

    def summarize(self, items: List[Union[dict, str]]) -> str:
        """
        Summarize a list of items.

        Parameters
        ----------
        items : List[Union[dict, str]]
            List of items to summarize. Each item can be a string or a dictionary with a "query" key in metadata.

        Returns
        -------
        str
            The generated summary.
        """
        text = " ".join([item if isinstance(item, str)
                         else getattr(item, "metadata", "").get("query") for item in items])
        text = text[:MAX_LENGTH]

        prompt = f"Please summarize the following text:\n{text}\nSummary:"
        summary = self.llm.generate(prompt)

        return summary
