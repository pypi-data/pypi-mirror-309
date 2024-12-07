# tests/test_my_module.py

import unittest
from exchange_ob.exchanges import Binance,Bitmart,KuCoin

class TestMyModule(unittest.IsolatedAsyncioTestCase):
    
    async def test_binance_connection(self):
        binance = Binance()
        await binance.connect("BTC/USDT")
        # verify connection
        self.assertTrue(binance.is_connected)  

    async def test_bitmart_connection(self):
        bitmart = Bitmart()
        await bitmart.connect(symbol="BTC/USDT")
        # verify connection
        self.assertTrue(bitmart.is_connected) 

    async def test_kucoin_connection(self):
        kucoin = KuCoin()
        await kucoin.connect(symbol="BTC/USDT")
        # verify connection
        self.assertTrue(kucoin.is_connected) 
if __name__ == "__main__":
    unittest.main()
