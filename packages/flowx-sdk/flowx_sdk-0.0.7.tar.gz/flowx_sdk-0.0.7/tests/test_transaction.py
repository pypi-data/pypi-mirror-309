import unittest
from flowx_sdk.transaction import Transaction # type: ignore

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(network_url="https://api.sui.network")

    def test_send_payment(self):
        tx_info = self.transaction.send_payment(
            sender_wallet="sender_wallet_address",
            receiver_wallet="receiver_wallet_address",
            amount=100,
            stablecoin="USDC"
        )
        
        self.assertEqual("tx_id", tx_info)

    def test_get_transaction_status(self):
        status = self.transaction.get_transaction_status(tx_id="sample_tx_id")
        self.assertEqual(status, "completed")
