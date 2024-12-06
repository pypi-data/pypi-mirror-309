import os
from .auth.authenticator import CustomAuthenticator

# Fetch the API key from environment variables or any secure source
API_KEY = os.getenv("LLAMARCH_API_KEY")

# Auth server configuration
# Replace with your auth server URL
AUTH_SERVER_URL = "https://auth-server-av5b.onrender.com"
# Application name expected by auth server
APPLICATION_NAME = "llamarch"

# Initialize the CustomAuthenticator
authenticator = CustomAuthenticator(auth_server_url=AUTH_SERVER_URL)

# Check API key validity on package import
if API_KEY is None:
    print('No API key specified. You are agreeing to use the `llamarch` package for academic and personal use only.')
else:
    payload = authenticator.verify_api_key(API_KEY, APPLICATION_NAME)
    print("API key is valid.")
