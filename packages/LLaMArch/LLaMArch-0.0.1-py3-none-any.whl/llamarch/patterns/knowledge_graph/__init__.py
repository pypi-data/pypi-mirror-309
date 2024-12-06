from llamarch.common.llm import LLM
from llamarch.common.graph_db import GraphDB


class KnowledgeLLM:
    def __init__(self, knowledge_graph: GraphDB, llm: LLM):
        """
        Initialize the KnowledgeLLM with a knowledge graph and a language model.

        Parameters
        ----------
        knowledge_graph : GraphDB
            The knowledge graph instance that will be used to store and retrieve knowledge.
        llm : LLM
            The language model instance that will be used to generate ontologies and respond to queries.
        """
        self.knowledge_graph = knowledge_graph
        self.llm = llm

    def query_knowledge_graph(self, query):
        """
        Query the knowledge graph for relevant data.

        Parameters
        ----------
        query : str
            The query to be executed on the knowledge graph.

        Returns
        -------
        Any
            The result from the knowledge graph query.
        """
        return self.knowledge_graph.read_data(query)

    def update_knowledge_graph(self, query, parameters=None):
        """
        Update the knowledge graph with new data.

        Parameters
        ----------
        query : str
            The query to modify the knowledge graph (e.g., adding or updating nodes).
        parameters : dict, optional
            Optional parameters for the query (default is None).
        """
        self.knowledge_graph.write_data(query, parameters)

    def generate_ontology(self, text):
        """
        Generate an ontology from the provided text using the language model.

        Parameters
        ----------
        text : str
            The text from which the ontology will be generated.

        Returns
        -------
        str
            The generated ontology.

        Notes
        -----
        The generated ontology will be inserted into the knowledge graph.
        """
        prompt = f"Generate an ontology from the following text: {text}"
        ontology = self.llm.generate(prompt)
        # Insert the generated ontology into the knowledge graph
        self.update_knowledge_graph(
            "CREATE (n:Ontology {data: $ontology})", {"ontology": ontology})
        return ontology

    def respond_to_query(self, query):
        """
        Generate a response to a query by combining information from the knowledge graph and the language model.

        Parameters
        ----------
        query : str
            The query to be answered using both the knowledge graph and language model.

        Returns
        -------
        str
            The generated response to the query.

        Notes
        -----
        This method combines the results from a knowledge graph query with the language model's response.
        """
        graph_result = self.query_knowledge_graph(query)
        prompt = f"Given this knowledge: {graph_result}, answer the following query: {query}"
        print(prompt)
        return self.llm(prompt)
