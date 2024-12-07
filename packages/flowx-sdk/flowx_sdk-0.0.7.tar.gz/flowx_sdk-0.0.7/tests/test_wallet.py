import unittest
from flowx_sdk.wallets import Wallet #type: ignore

class TestWallet(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet(network_url="https://api.sui.network")

    def test_create_wallet(self):
        wallet_info = self.wallet.create_wallet()
        self.assertEqual("address", wallet_info)

    def test_get_balance(self):
        balance = self.wallet.get_wallet_balance(wallet_address="sample_wallet_address")
        self.assertEqual(balance, 0)
