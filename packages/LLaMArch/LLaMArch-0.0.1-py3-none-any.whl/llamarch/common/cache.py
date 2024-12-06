import redis


class Cache:
    """
    A simple cache class using Redis as the backend.

    Parameters
    ----------
    host : str, optional
        The hostname of the Redis server (default is "localhost").
    port : int, optional
        The port number on which the Redis server is running (default is 6379).
    db : int, optional
        The Redis database number to use (default is 0).

    Attributes
    ----------
    client : redis.Redis
        The Redis client instance used to interact with the Redis server.
    """

    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key: str, value: str, expiration: int = None):
        """
        Set a key-value pair in the cache with an optional expiration.

        Parameters
        ----------
        key : str
            The key under which the value will be stored.
        value : str
            The value to store in the cache.
        expiration : int, optional
            The time-to-live (TTL) for the key in seconds. If not provided, the key will persist indefinitely.

        Returns
        -------
        bool
            Returns True if the operation is successful, False otherwise.
        """
        return self.client.set(key, value, ex=expiration)

    def get(self, key: str):
        """
        Retrieve the value associated with a key from the cache.

        Parameters
        ----------
        key : str
            The key to retrieve the value for.

        Returns
        -------
        str or None
            The value associated with the key, or None if the key does not exist.
        """
        value = self.client.get(key)
        return value.decode('utf-8') if value else None

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair from the cache.

        Parameters
        ----------
        key : str
            The key to delete.

        Returns
        -------
        bool
            Returns True if the key was deleted, False if the key does not exist.
        """
        return self.client.delete(key) > 0

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Parameters
        ----------
        key : str
            The key to check for existence.

        Returns
        -------
        bool
            Returns True if the key exists, False otherwise.
        """
        return self.client.exists(key) == 1

    def get_all_values(self) -> list:
        """
        Retrieve all values stored in the cache.

        Returns
        -------
        list of str
            A list of all values currently stored in the cache as strings.
        """
        keys = self.client.keys('*')  # Get all keys
        return [self.client.get(key).decode('utf-8') for key in keys if self.client.exists(key)]
