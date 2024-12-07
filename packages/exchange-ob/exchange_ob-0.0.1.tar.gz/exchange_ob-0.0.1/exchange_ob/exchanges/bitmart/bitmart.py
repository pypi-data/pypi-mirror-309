import json
import asyncio
import websockets
from typing import Optional
from exchange_ob.config import Config
from exchange_ob.exchanges.order_book import OrderBook

class Bitmart:
    allowed_levels = {5, 20, 50} 
    def __init__(self, symbol: str, level: int = 20):
        self.symbol = symbol.replace("/", "_")
        if level not in self.allowed_levels:
            print(f"Invalid level {level}. Allowed levels are {self.allowed_levels}. Setting default level to 20.")
            self.level = 20
        else:
            self.level = level
        self.ws_url = Config.BITMART_BASE_URL
        self.latest_order_book = OrderBook()

    async def connect(self):
        while True:  # Loop to reconnect on disconnection
            try:
             async with websockets.connect(self.ws_url) as websocket:
                    print(f"Connected to BitMart WebSocket for {self.symbol} order book.")
                    # Subscribe to the order book channel
                    await self.subscribe_to_order_book(websocket)

                    async for message in websocket:
                        data = json.loads(message)
                        if "error" in data:
                            print("Subscription error:", data["error"])
                        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                            order_data = data["data"][0] 
                            if "asks" in order_data and "bids" in order_data:
                                asks = order_data["asks"]
                                bids = order_data["bids"]
                                self.latest_order_book.update(bids, asks)
                                
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Disconnected from BitMart. Reconnecting...: {e}")
                await asyncio.sleep(1)

    async def subscribe_to_order_book(self, websocket):
            # Construct the subscription message for BitMart
            subscription_message = {
                "op": "subscribe",
                "args": [f"spot/depth{self.level}:{self.symbol}"] 
            }
            await websocket.send(json.dumps(subscription_message))
            print(f"Subscribed to {self.symbol} order book on BitMart.")

    def get_order_book(self) -> Optional[OrderBook]:
        return self.latest_order_book

