# Wallet creation and management

import requests #type: ignore

class Wallet:
    def __init__(self, network_url):
        self.network_url = network_url

    def create_wallet(self):
        """Create a new wallet."""
        # response = requests.post(f'{self.network_url}/create_wallet')
        # if response.status_code == 200:
        #     return response.json()  # Return wallet info
        # else:
        #     raise Exception("Failed to create wallet")
        return "address"

    def get_wallet_balance(self, wallet_address):
        """Get the balance of a wallet."""
        print("this is the wallet balance")
        return 0
        # response = requests.get(f'{self.network_url}/wallet/{wallet_address}/balance')
        # if response.status_code == 200:
        #     return response.json()  # Return wallet balance
        # else:
        #     raise Exception("Failed to fetch wallet balance")
