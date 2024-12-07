from .core.config import settings
import requests #type: ignore

class Client:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._base_url = settings.base_url
        self.authenticate = False #type: ignore

        # Initialize the http client (requests)
        self.session = requests.Session()

        # Attempt to authenticate on initialization
        self.authenticate()
    

    def authenticate(self):
        """Authenticate with the API using the provided API key."""
        auth_url = f"{self._base_url}/auth"
        headers = {"X-Token": self.api_key} # Use X-Token header for authentication

        # end a GET or POST request to verify the API key
        response = self.session.get(auth_url, headers=headers)

        if response.status_code == 200:
            self.authenticate = True
            print(f"Authenticated successfully")
        else:
            self.authenticate = False
            print("Authentication failed")