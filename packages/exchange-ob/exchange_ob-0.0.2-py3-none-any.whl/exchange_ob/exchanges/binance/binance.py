import json
import asyncio
import websockets
from typing import Optional
from exchange_ob.config import Config
from exchange_ob.exchanges.order_book import OrderBook

class Binance:
    def __init__(self):
        self.ws_url = None
        self.latest_order_book = OrderBook()

    async def connect(self, symbol: str, level: int = 20):
        self.symbol = symbol.replace("/", "").lower()
        self.level = level
        self.ws_url = f"{Config.BINANCE_BASE_URL}/{self.symbol}@depth{self.level}@100ms"

        while True:  # Loop to reconnect on disconnection
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    print(f"Connected to Binance WebSocket for {self.symbol} order book.")
                    async for message in websocket:
                        data = json.loads(message)
                        bids = data.get("bids", [])
                        asks = data.get("asks", [])
                        self.latest_order_book.update(bids, asks)
                        # Print the order book
                        # print("\nOrder Book Update:")
                        # print("\nAsks:")
                        # for price, quantity in self.latest_order_book.asks:
                        #     print(f"Price: {price}, Quantity: {quantity}")

                        # print("\nBids:")
                        # for price, quantity in self.latest_order_book.bids:
                        #     print(f"Price: {price}, Quantity: {quantity}")

                        # print("------------------------------")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Disconnected from Binance. Reconnecting...: {e}")
                await asyncio.sleep(1)

    def get_order_book(self) -> Optional[OrderBook]:
        return self.latest_order_book
