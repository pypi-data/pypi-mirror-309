# tests/test_my_module.py

import unittest
from exchange_ob.exchanges import Binance,Bitmart,KuCoin

class TestMyModule(unittest.IsolatedAsyncioTestCase):
    
    async def test_binance_connection(self):
        binance = Binance(symbol="BTC/USDT")
        await binance.connect()
        # You can add assertions here to verify connection
        self.assertTrue(binance.is_connected)  

    async def test_bitmart_connection(self):
        bitmart = Bitmart(symbol="BTC/USDT")
        await bitmart.connect()
        # You can add assertions here to verify connection
        self.assertTrue(bitmart.is_connected) 

    async def test_kucoin_connection(self):
        kucoin = KuCoin(symbol="BTC/USDT")
        await kucoin.connect()
        # You can add assertions here to verify connection
        self.assertTrue(kucoin.is_connected) 
if __name__ == "__main__":
    unittest.main()
