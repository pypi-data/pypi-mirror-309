from typing import List


class LongTermMemory:
    def __init__(self, vector_db_client: 'VectorDB'):
        """
        Initialize the LongTermMemory with a vector database client for long-term storage.

        Parameters
        ----------
        vector_db_client : VectorDB
            An instance of the VectorDB class that will be used for long-term storage of embeddings.
        """
        self.vector_db = vector_db_client

    def store_information(self, vectors: List[List[float]], ids: List[str]):
        """
        Store embeddings in long-term memory using the vector database.

        Parameters
        ----------
        vectors : List[List[float]]
            A list of embeddings (vectors) to store in the long-term memory.
        ids : List[str]
            A list of unique identifiers corresponding to each embedding.

        Notes
        -----
        This method iterates over the `vectors` and `ids`, storing each embedding with its associated unique identifier.
        """
        for vector_id, embedding in zip(ids, vectors):
            self.vector_db.add_embeddings(vector_id, embedding)

    def fetch_similar(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        """
        Fetch similar embeddings from long-term memory.

        Parameters
        ----------
        query_vector : List[float]
            The embedding vector to search for similar vectors.
        top_k : int, optional
            The number of similar vectors to retrieve (default is 5).

        Returns
        -------
        List[dict]
            A list of results, each containing similar embedding data from the vector database.

        Notes
        -----
        The method uses the vector database to find the `top_k` most similar embeddings to the `query_vector`.
        """
        return self.vector_db.query_similar(query_vector, top_k)
