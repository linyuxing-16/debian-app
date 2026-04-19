import websocket_class
from config import WS_URL, WS_AUTH_ENABLED, WS_AUTH_TOKEN
from base import Receiver
import sys
import json
from PyQt5.QtWidgets import QApplication
import pet_ui
import chat_ui
import threading
import textarea

app = QApplication(sys.argv)

websocket_client = websocket_class.WebSocketClient(WS_URL, WS_AUTH_ENABLED, WS_AUTH_TOKEN)

receiver = Receiver()

def receive_message():
    i = ""
    while True:
        message = websocket_client.get_message()
        data = json.loads(message)

        # 思考消息（reasoning）不累积内容，但触发宠物说话动画
        if data.get("type") == "reasoning":
            receiver.signal.emit(i, "reasoning")
        # 普通文本消息，累积内容
        elif data.get("type") == "message" and data.get("content") is not None:
            content = data["content"]
            # content 可以是字符串或内容对象列表
            if isinstance(content, str):
                i += content
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        i += item.get("text", "")
                    elif isinstance(item, str):
                        i += item
            receiver.signal.emit(i, "type")
        # 事件消息，重置累积变量
        elif "event" in data:
            i = ""
            receiver.signal.emit(i, "event")

def receive_message_type(message, type):
    if type == "type":
        window_pet.startTalking()
    elif type == "reasoning":
        window_pet.startTalking()
    elif type == "event":
        window_pet.resetExpression()

def send_message():
    while True:
        message = windows_textarea.get_message()
        websocket_client.send(message)


t1 = threading.Thread(target=receive_message, daemon=True)
t2 = threading.Thread(target=send_message, daemon=True)
window_pet = pet_ui.pet_window()
window_chat = chat_ui.pet_window()
windows_textarea = textarea.textarea()
receiver.signal.connect(window_chat.chat)
receiver.signal.connect(receive_message_type)
t1.start()
t2.start()
window_chat.show()
window_pet.show()
windows_textarea.show()

sys.exit(app.exec())