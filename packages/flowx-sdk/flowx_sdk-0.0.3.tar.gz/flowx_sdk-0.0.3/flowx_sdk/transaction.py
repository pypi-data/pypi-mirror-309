import requests #type: ignore

class Transaction:
    def __init__(self, network_url):
        self.network_url = network_url

    def send_payment(self, sender_wallet, receiver_wallet, amount, stablecoin="USDC"):
        """Send payment from one wallet to another."""
        data = {
            "sender": sender_wallet,
            "receiver": receiver_wallet,
            "amount": amount,
            "stablecoin": stablecoin
        }
        # response = requests.post(f'{self.network_url}/send_payment', json=data)
        # if response.status_code == 200:
        #     return response.json()  # Return transaction info
        # else:
        #     raise Exception("Failed to send payment")
        return "tx_id"


    def get_transaction_status(self, tx_id):
        """Fetch the status of a transaction."""
        # response = requests.get(f'{self.network_url}/transaction/{tx_id}/status')
        # if response.status_code == 200:
        #     return response.json()  # Return transaction status
        # else:
        #     raise Exception("Failed to fetch transaction status")
        return "completed"
