import requests


class CustomAuthenticator:
    def __init__(self, auth_server_url):
        """
        Initialize the Custom Authenticator.

        Args:
            auth_server_url (str): URL of the custom authentication server.
        """
        self.auth_server_url = auth_server_url

    def verify_api_key(self, token, application_name):
        """
        Verify the provided API key (JWT) by querying the custom auth server.

        Args:
            token (str): The JWT token to verify.
            application_name (str): The name of the application to verify.

        Returns:
            dict: Response from the auth server if verification is successful.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        # Send the token to the FastAPI auth server's verify endpoint
        try:
            response = requests.post(
                f"{self.auth_server_url}/verify",
                json={"token": token, "application_name": application_name}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(
                    f"Token validation failed: {response.json().get('detail', 'Unknown error')}")
        except requests.RequestException as e:
            raise ValueError("Failed to connect to the auth server") from e
