from typing import List, Union


class VectorDB:
    def __init__(self, db_type="qdrant", api_key=None, environment=None, index_name="default_index", embedding_model=None):
        """
        Initialize the vector database client. Currently defaulting only to Qdrant.

        Parameters
        ----------
        db_type : str, optional
            Type of vector database. Default is 'qdrant'.
        api_key : str, optional
            API key for the vector database (if required).
        environment : str, optional
            Environment or URL for the vector database (if required).
        index_name : str, optional
            Name of the index or collection in the vector database. Default is 'default_index'.
        embedding_model : optional
            Required for Qdrant, the embedding model used.
        """
        self.db_type = db_type.lower()
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.client = self._initialize_client()

    def _initialize_client(self):
        """
        Initialize the client for the specified vector database type.

        Returns
        -------
        object
            The initialized client for the selected vector database.

        Raises
        ------
        ValueError
            If an unsupported db_type is provided.
        """
        if self.db_type == "qdrant":
            from qdrant_client import QdrantClient
            from langchain_qdrant import QdrantVectorStore
            client = QdrantClient(api_key=self.api_key, url=self.environment)
            return QdrantVectorStore(client=client, collection_name=self.index_name, embedding=self.embedding_model)

        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")

    def add_embeddings(self, vector_id: str, embedding: List[float], metadata: dict = None):
        """
        Add an embedding to the vector database.

        Parameters
        ----------
        vector_id : str
            Unique identifier for the vector.
        embedding : List[float]
            The embedding vector to add to the database.
        metadata : dict, optional
            Additional metadata to store with the vector. Default is None.
        """
        self.client.add_texts(
            texts=[str(embedding)],
            metadatas=[metadata],
            ids=[vector_id]
        )

    def query_similar(self, embedding: List[float], top_k: int = 5) -> List[Union[dict, str]]:
        """
        Query for similar embeddings in the vector database.

        Parameters
        ----------
        embedding : List[float]
            The embedding vector to search for similar vectors.
        top_k : int, optional
            Number of similar vectors to retrieve. Default is 5.

        Returns
        -------
        List[Union[dict, str]]
            List of results from the vector database, typically containing metadata and vector information.
        """
        results = self.client.similarity_search_by_vector(embedding, k=top_k)
        return results
