# Liquidity management

import requests #type: ignore

class Liquidity:
    def __init__(self, network_url):
        self.network_url = network_url

    def add_liquidity(self, wallet_address, pool_id, amount, stablecoin="USDC"):
        """Add liquidity to a pool."""
        data = {
            "wallet_address": wallet_address,
            "pool_id": pool_id,
            "amount": amount,
            "stablecoin": stablecoin
        }
        print(f"{data} added ok")
        return 200
        # response = requests.post(f'{self.network_url}/add_liquidity', json=data)
        # if response.status_code == 200:
        #     return response.json()  # Return liquidity update info
        # else:
        #     raise Exception("Failed to add liquidity")
