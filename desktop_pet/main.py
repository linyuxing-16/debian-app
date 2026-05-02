import websocket_class
from config import WS_URL, WS_AUTH_ENABLED, WS_AUTH_TOKEN
from base import Receiver
import sys
import json
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pet_ui
import dialog
import threading
import pettraylcon
import settings_ui


def receive_message():
    i = ""
    while True:
        if not websocket_client.is_connected():
            time.sleep(0.1)
            continue
        try:
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
        except Exception:
            continue


def receive_message_type(message, type):
    if type == "type":
        window_pet.startTalking()
    elif type == "reasoning":
        window_pet.startTalking()
    elif type == "event":
        window_pet.resetExpression()


def send_message():
    while True:
        message = window_dialog.get_message()
        websocket_client.send(message)


# 应用入口
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)  # 关闭所有窗口后不退出程序

receiver = Receiver()

# 先创建 UI 窗口
window_dialog = dialog.DialogWindow()
window_settings = settings_ui.SettingsWindow()
window_pet = pet_ui.pet_window(window_dialog, window_settings)
receiver.signal.connect(window_dialog.chat)
receiver.signal.connect(receive_message_type)

# 显示窗口
window_dialog.show()
window_pet.show()

# 创建托盘图标
tray = pettraylcon.Traylcon(window_pet, window_dialog, window_settings)
tray.show()

# 创建 WebSocket 客户端（不阻塞）
websocket_client = websocket_class.WebSocketClient(WS_URL, WS_AUTH_ENABLED, WS_AUTH_TOKEN)

# 启动后台线程
t1 = threading.Thread(target=receive_message, daemon=True)
t2 = threading.Thread(target=send_message, daemon=True)
t1.start()
t2.start()

# 异步连接 WebSocket
websocket_client.connect_async()

# 设置 dialog 的 websocket 客户端引用
window_dialog.set_websocket_client(websocket_client)
window_dialog.set_pet_window(window_pet)

# 创建定时器更新连接状态
status_timer = QTimer()
status_timer.timeout.connect(window_dialog.update_connection_status)
status_timer.start(1000)  # 每 1 秒更新一次

sys.exit(app.exec())
