class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

    def update(self, bids, asks):
        self.bids = bids
        self.asks = asks

    def get_order_book(self):
        if not self.bids or not self.asks:
            print("Order book not yet available.")
            return None
        return {"bids": self.bids, "asks": self.asks}