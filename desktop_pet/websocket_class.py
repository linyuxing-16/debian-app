import websocket
import queue
import threading
import time
from urllib.parse import urlencode


class ConnectionAuthError(Exception):
    """认证错误异常"""
    pass


class WebSocketClient:
    def __init__(self, url, auth_enabled=False, auth_token="", timeout=5, reconnect_interval=3):
        self.url = self._build_url(url, auth_enabled, auth_token)
        self.ws = None
        self.q = queue.Queue()
        self.timeout = timeout
        self.reconnect_interval = reconnect_interval
        self._connected = False
        self._connecting = False
        self._running = True

    def connect_async(self):
        """在后台线程中异步建立连接"""
        if self._connecting or self._connected:
            return
        thread = threading.Thread(target=self._connect_with_retry, daemon=True)
        thread.start()

    def _connect_with_retry(self):
        """带重试的连接逻辑"""
        self._connecting = True
        while self._running:
            try:
                self.ws = websocket.WebSocket()
                self.ws.settimeout(self.timeout)
                self.ws.connect(self.url)
                self._connected = True
                self._connecting = False
                threading.Thread(target=self._receive_loop, daemon=True).start()
                return
            except Exception:
                if not self._running:
                    break
                time.sleep(self.reconnect_interval)
        self._connecting = False

    def _receive_loop(self):
        """接收消息循环"""
        while self._connected:
            try:
                message = self.ws.recv()
                self.q.put(message)
            except Exception:
                break
        self._connected = False

    def _build_url(self, base_url, auth_enabled, auth_token):
        """构建带认证 token 的 URL"""
        if auth_enabled and auth_token:
            separator = "&" if "?" in base_url else "?"
            return f"{base_url}{separator}token={auth_token}"
        return base_url

    def is_connected(self):
        """检查是否已连接"""
        return self._connected

    def send(self, text):
        """发送消息"""
        if not self._connected or self.ws is None:
            return
        try:
            self.ws.send(text)
        except Exception:
            pass

    def get_message(self):
        """获取消息（会阻塞直到有消息）"""
        return self.q.get()
        
