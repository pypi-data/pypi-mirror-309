import requests

class Config:
    BINANCE_BASE_URL = "wss://stream.binance.com:9443/ws"
    BITMART_BASE_URL = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1"
    KUCOIN_TOKEN_URL = "https://api.kucoin.com/api/v1/bullet-public"

    @staticmethod
    def get_kucoin_ws_url() -> str:
        # Request a new token from KuCoin's REST API
        response = requests.post(Config.KUCOIN_TOKEN_URL)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == "200000":
                token = data["data"]["token"]
                instance_server = data["data"]["instanceServers"][0]["endpoint"]
                return f"{instance_server}?token={token}"
            else:
                raise Exception("Failed to fetch WebSocket token from KuCoin API.")
        else:
            raise Exception(f"Error requesting WebSocket token: {response.status_code}")
