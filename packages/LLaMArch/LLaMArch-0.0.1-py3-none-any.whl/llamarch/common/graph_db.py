# Replace with a library appropriate to your graph DB
from neo4j import GraphDatabase


class GraphDB:
    """
    A class for interacting with a Neo4j graph database.

    Parameters
    ----------
    uri : str
        The URI of the Neo4j database.
    user : str
        The username for authentication.
    password : str
        The password for authentication.

    Attributes
    ----------
    driver : neo4j.Driver
        The Neo4j driver instance for managing database connections.
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Close the connection to the Neo4j database.

        Returns
        -------
        None
        """
        self.driver.close()

    def write_data(self, query: str, parameters: dict = None):
        """
        Execute a write query on the Neo4j database.

        Parameters
        ----------
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        None
        """
        with self.driver.session() as session:
            session.write_transaction(self._execute_query, query, parameters)

    def read_data(self, query: str, parameters: dict = None) -> list:
        """
        Execute a read query on the Neo4j database and return the results.

        Parameters
        ----------
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        list
            A list of records returned by the query.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                self._execute_query, query, parameters)
            return list(result)

    @staticmethod
    def _execute_query(tx, query: str, parameters: dict = None):
        """
        Helper method to execute a query within a transaction.

        Parameters
        ----------
        tx : neo4j.Transaction
            The transaction object.
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        neo4j.Result
            The result of the query execution.
        """
        return tx.run(query, parameters)

    def write_key_value(self, key: str, value: str):
        """
        Execute a write query on the Neo4j database.

        Parameters
        ----------
        key : str
            The key to be used to store the value
        value : str
            The value to be stored

        Returns
        -------
        None
        """
        with self.driver.session() as session:
            query = """
            MERGE (n:Data {key: $key})
            SET n.value = $value
            RETURN n
            """
            result = session.run(query, key=key, value=value)

            # Print the result (the created or updated node)
            for record in result:
                print(f"Upserted Node: {record['n']}")

    def read_by_value(self, value: str) -> list:
        """
        Execute a read on the Neo4j database to find nodes based on the value.

        Parameters
        ----------
        value : str
            The value to search for in the database

        Returns
        -------
        str
            The key associated with the value if found, else None
        """
        with self.driver.session() as session:
            query = """
            MATCH (n:Data {value: $value})
            RETURN n.key AS key
            """
            result = session.run(query, value=value)

            # Return the key if the node is found, otherwise None
            for record in result:
                return record["key"]

        # If no key is found for the value, return None
        return None
