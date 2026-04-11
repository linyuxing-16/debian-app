import websocket
from config import WS_URL
import json
import pet_ui
import threading
from PyQt5.QtWidgets import QApplication

websocket_client = websocket.WebSocketClient(WS_URL)
window_pet = pet_ui.pet_window()
window_pet.show()

def receive_message():
    import chat_ui
    window = chat_ui.pet_window()
    while True:
        message = websocket_client.get_message()
        data = json.loads(message)
        if "type" in data:
            window_pet.startTalking()
            window_pet.show()
            window.chat(data["content"])
            window.show()
        elif "event" in data:
            window.chat(data["content"])
            window.show()
            window_pet.startThinking()
            window_pet.show()

def send_message():
    import textarea
    window = textarea.textarea()
    window.show()
    message = window.get_message()
    websocket_client.send(message)

if __name__ == "__main__":
    import sys
    t1 = threading.Thread(target=receive_message, daemon=True)
    t2 = threading.Thread(target=send_message, daemon=True)
    t1.start()
    t2.start()
    app = QApplication(sys.argv)
    sys.exit(app.exec_())
