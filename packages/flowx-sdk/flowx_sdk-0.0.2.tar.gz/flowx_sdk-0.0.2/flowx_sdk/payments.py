# Payment-related functions


import requests #type: ignore

class FlowXPayments:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def send_payment(self, sender_wallet, receiver_wallet, amount, stablecoin="USDC"):
        payload = {
            "sender_wallet": sender_wallet,
            "receiver_wallet": receiver_wallet,
            "amount": amount,
            "stablecoin": stablecoin
        }
        print(f"{payload} payment made")
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = requests.post(f"{self.api_url}/payments", json=payload, headers=headers)
        # return response.json()

    def get_transaction_status(self, tx_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = requests.get(f"{self.api_url}/payments/{tx_id}", headers=headers)
        # return response.json()
        print(f"{tx_id} this is the transaction")
