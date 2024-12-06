from typing import Any


class MemoryDecay:
    def __init__(self, importance_threshold=0.5):
        """
        Initialize the MemoryDecay component with an importance threshold for information retention.

        Parameters
        ----------
        importance_threshold : float, optional
            A threshold between 0 and 1 for deciding if information is important enough to retain, 
            by default 0.5.
        """
        self.importance_threshold = importance_threshold

    def evaluate(self, summary: str) -> bool:
        """
        Evaluate if a given summary is important enough to store in Long-Term Memory.

        Parameters
        ----------
        summary : str
            The summarized text to evaluate based on predefined importance criteria.

        Returns
        -------
        bool
            True if the summary meets the importance threshold and should be stored in Long-Term Memory, 
            False otherwise.

        Notes
        -----
        The evaluation is performed by checking for specific keywords (e.g., "important", "critical") 
        in the summary text. The importance score is calculated as the fraction of keywords found in the 
        summary, and if it meets or exceeds the importance threshold, the summary is deemed significant enough 
        to retain.
        """
        # Example heuristic: Check if certain keywords are in the summary
        important_keywords = ["important", "critical", "relevant", "necessary"]
        score = sum(1 for word in important_keywords if word in summary.lower(
        )) / len(important_keywords)

        # Decision based on threshold
        return score >= self.importance_threshold
