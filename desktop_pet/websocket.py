import websocket
import queue
import threading

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = websocket.WebSocket()
        self.ws.connect(self.url)
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.receive, daemon=True)
        self.thread.start()
    
    def send(self, message):
        self.ws.send(message)
    
    def receive(self):
        while True:
            message = self.ws.recv()
            self.q.put(message)
        
    def get_message(self):
        return self.q.get()
        
