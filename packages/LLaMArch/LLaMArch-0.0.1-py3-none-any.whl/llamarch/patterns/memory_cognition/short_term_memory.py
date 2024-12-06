import uuid
from .long_term_memory import LongTermMemory
from typing import List, Tuple
from llamarch.common.vector_db import VectorDB


class ShortTermMemory:
    def __init__(self, vector_db_client: VectorDB):
        """
        Initialize the ShortTermMemory with a vector database client for temporary storage.

        Parameters
        ----------
        vector_db_client : VectorDB
            An instance of the VectorDB class that will be used for short-term storage of embeddings.
        """
        self.vector_db = vector_db_client
        # Temporary list for embeddings
        self.temp_store: List[Tuple[str, List[float]]] = []

    def store_information(self, vector: List[float], query: str):
        """
        Store an embedding in short-term memory and add it to the vector database.

        Parameters
        ----------
        vector : List[float]
            The embedding vector to store in short-term memory.
        query : str
            The original query or context associated with the embedding.

        Notes
        -----
        This method generates a unique ID for each embedding, stores the embedding in a temporary list, and
        adds it to the vector database with the associated query as metadata.
        """
        info_id = str(uuid.uuid4())
        # Store ID, vector, and query
        self.temp_store.append((info_id, vector, query))
        self.vector_db.add_embeddings(
            info_id, vector, metadata={'query': query})

    def fetch_similar(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        """
        Search for similar embeddings in short-term memory.

        Parameters
        ----------
        query_vector : List[float]
            The embedding vector to search for similar vectors.
        top_k : int, optional
            The number of similar vectors to retrieve (default is 5).

        Returns
        -------
        List[dict]
            A list of results containing similar embedding data from the vector database.

        Notes
        -----
        This method queries the vector database for the `top_k` most similar embeddings to the provided
        `query_vector` and returns the results.
        """
        return self.vector_db.query_similar(query_vector, top_k)

    def flush_to_long_term(self, long_term_memory: LongTermMemory):
        """
        Move temporary embeddings from short-term memory to long-term memory.

        Parameters
        ----------
        long_term_memory : LongTermMemory
            An instance of LongTermMemory where the embeddings will be stored.

        Notes
        -----
        This method transfers all stored embeddings from short-term memory to long-term memory and then clears
        the temporary store to free up space for new data.
        """
        if self.temp_store:
            ids, vectors = zip(*self.temp_store)
            long_term_memory.store_information(vectors, ids)
            self.temp_store.clear()  # Clear short-term memory
