import json
import asyncio
import websockets
from typing import Optional
from exchange_ob.config import Config
from exchange_ob.exchanges.order_book import OrderBook

class KuCoin:
    allowed_levels = {5,50} 
    def __init__(self, symbol: str, level:int = 5):
        self.symbol = symbol.replace("/", "-")  # KuCoin expects symbols like "BTC-USDT"
        if level not in self.allowed_levels:
            print(f"Invalid level {level}. Allowed levels are {self.allowed_levels}. Setting default level to 5.")
            self.level = 5
        else:
            self.level = level
        self.ws_url = Config.get_kucoin_ws_url()  
        self.latest_order_book = OrderBook()

    async def connect(self):
        while True:  # Loop to reconnect on disconnection
            try:
                async with websockets.connect(self.ws_url, ping_interval=None) as websocket:
                    print(f"Connected to KuCoin WebSocket for {self.symbol} order book.")
                    
                    # Start listening to pings to keep the connection alive
                    asyncio.create_task(self.send_ping(websocket))

                    # Subscribe to the level2 order book channel
                    await self.subscribe_to_order_book(websocket)

                    async for message in websocket:
                        data = json.loads(message)
                        if "data" in data and "asks" in data["data"] and "bids" in data["data"]:
                            asks = data["data"]["asks"]
                            bids = data["data"]["bids"]
                            self.latest_order_book.update(bids, asks)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed: {e}. Reconnecting...")
                await asyncio.sleep(5)  # Wait before attempting to reconnect

    async def subscribe_to_order_book(self, websocket):
        subscription_message = {
            "id": "1",
            "type": "subscribe",
            "topic": f"/spotMarket/level2Depth{self.level}:{self.symbol}",
            "privateChannel": False,
            "response": True
        }
        await websocket.send(json.dumps(subscription_message))
        print(f"Subscribed to {self.symbol} order book on KuCoin.")

    async def send_ping(self, websocket):
        while True:
            try:
                await websocket.ping()
                await asyncio.sleep(30)  # Ping every 30 seconds
            except websockets.ConnectionClosed:
                print("Connection closed while sending ping.")
                break

    def get_order_book(self) -> Optional[OrderBook]:
        return self.latest_order_book
