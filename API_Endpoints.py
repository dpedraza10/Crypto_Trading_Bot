# Packages
import websocket, json
import config
import time
from collections import deque

# Global Variables
X = deque(maxlen = 20)

# Websocket Class
class api:
    def __init__(self): 
        socket = config.WEBSOCKET
        self.ws = websocket.WebSocketApp(socket, on_open=self.on_open, on_message=self.on_message)
        self.ws.run_forever()

    def on_open(self, ws):
        auth_data = {
            "action": "auth",
            "key": config.ALPACA_API_KEY, 
            "secret": config.ALPACA_SECRET_KEY
        }

        ws.send(json.dumps(auth_data))

        listen_message = {"action":"subscribe","trades":["BTCUSD"]}

        ws.send(json.dumps(listen_message))

    def on_message(self, ws, message):

        time.sleep(1)

        prices = json.loads(message)[0]
        print(prices)


if __name__=="__main__":
    Api = api()