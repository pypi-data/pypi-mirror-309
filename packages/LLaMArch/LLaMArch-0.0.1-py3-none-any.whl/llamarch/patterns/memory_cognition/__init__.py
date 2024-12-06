import logging


class MemoryCognition:
    """
    A class to handle memory processing, including storing, retrieving, summarizing, 
    and evaluating information from short-term and long-term memory.

    Attributes
    ----------
    llm : object
        The large language model used for processing.
    embedding : object
        The embedding used for representing queries.
    short_term_memory : object
        The short-term memory system for storing and retrieving data.
    long_term_memory : object
        The long-term memory system for storing and retrieving data.
    summarizer : object
        The summarizer used to summarize similar items from memory.
    memory_decay : object
        The system used to evaluate memory decay.
    logger : logging.Logger
        Logger for the MemoryCognition class.
    """

    def __init__(self, llm, embedding, short_term_memory, long_term_memory, summarizer, memory_decay):
        """
        Initializes the MemoryCognition instance with the provided components.

        Parameters
        ----------
        llm : object
            The large language model used for processing.
        embedding : object
            The embedding used for representing queries.
        short_term_memory : object
            The short-term memory system for storing and retrieving data.
        long_term_memory : object
            The long-term memory system for storing and retrieving data.
        summarizer : object
            The summarizer used to summarize similar items from memory.
        memory_decay : object
            The system used to evaluate memory decay.
        """
        self.llm = llm
        self.embedding = embedding
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory
        self.summarizer = summarizer
        self.memory_decay = memory_decay
        self.logger = logging.getLogger(__name__)
        self.logger.info("MemoryCognition initialized.")

    def store_information(self, query, query_vector):
        """
        Store information in short-term memory.

        Parameters
        ----------
        query : str
            The query text to be stored in memory.
        query_vector : numpy.ndarray
            The vector representation of the query to be stored in memory.
        """
        self.short_term_memory.store_information(query_vector, query)
        self.logger.info(f"Information stored in Short-Term Memory: {query}")

    def fetch_similar(self, query_vector):
        """
        Fetch similar items from short-term memory based on the query vector.

        Parameters
        ----------
        query_vector : numpy.ndarray
            The vector representation of the query to search for similar items.

        Returns
        -------
        list
            A list of similar items found in short-term memory.
        """
        similar_items_stm = self.short_term_memory.fetch_similar(query_vector)
        self.logger.info(
            f"Similar items in Short-Term Memory: {[getattr(x, 'metadata', {}).get('query') for x in similar_items_stm]}")
        return similar_items_stm

    def summarize(self, similar_items_stm):
        """
        Summarize the similar items fetched from short-term memory.

        Parameters
        ----------
        similar_items_stm : list
            A list of similar items from short-term memory to be summarized.

        Returns
        -------
        str
            A summary of the similar items.
        """
        summary = self.summarizer.summarize(similar_items_stm)
        self.logger.info(f"Summary of similar items: {summary}")
        return summary

    def evaluate(self, summary):
        """
        Evaluate the summary based on memory decay.

        Parameters
        ----------
        summary : str
            The summary of similar items to be evaluated.

        Returns
        -------
        float
            The evaluation result based on memory decay.
        """
        evaluation = self.memory_decay.evaluate(summary)
        self.logger.info(f"Evaluation: {evaluation}")
        return evaluation

    def flush_to_long_term(self, long_term_memory):
        """
        Flush the short-term memory content to long-term memory.

        Parameters
        ----------
        long_term_memory : object
            The long-term memory system to store the flushed data.
        """
        self.short_term_memory.flush_to_long_term(long_term_memory)
        self.logger.info("Summary flushed to Long-Term Memory.")

    def fetch_similar_from_long_term(self, query_vector):
        """
        Fetch similar items from long-term memory based on the query vector.

        Parameters
        ----------
        query_vector : numpy.ndarray
            The vector representation of the query to search for similar items.

        Returns
        -------
        list
            A list of similar items found in long-term memory.
        """
        long_term_results = self.long_term_memory.fetch_similar(query_vector)
        self.logger.info(
            f"Similar items in Long-Term Memory: {long_term_results}")
