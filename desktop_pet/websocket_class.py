import websocket
import queue
import threading
from urllib.parse import urlencode


class ConnectionAuthError(Exception):
    """认证错误异常"""
    pass


class WebSocketClient:
    def __init__(self, url, auth_enabled=False, auth_token=""):
        self.url = self._build_url(url, auth_enabled, auth_token)
        self.ws = websocket.WebSocket()
        try:
            self.ws.connect(self.url)
        except websocket.WebSocketBadStatusException as e:
            if e.status_code == 1008:
                raise ConnectionAuthError("认证失败：token 无效或缺失")
            raise ConnectionError(f"连接失败: {e}")
        except websocket.WebSocketTimeoutException:
            raise ConnectionError("连接超时")
        except Exception as e:
            raise ConnectionError(f"连接异常: {e}")

        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.receive, daemon=True)
        self.thread.start()

    def _build_url(self, base_url, auth_enabled, auth_token):
        """构建带认证 token 的 URL"""
        if auth_enabled and auth_token:
            separator = "&" if "?" in base_url else "?"
            return f"{base_url}{separator}token={auth_token}"
        return base_url

    def send(self, text):
        self.ws.send(text)

    def receive(self):
        while True:
            try:
                message = self.ws.recv()
                self.q.put(message)
            except Exception:
                break

    def get_message(self):
        return self.q.get()
        
