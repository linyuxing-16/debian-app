import os

WS_URL = "ws://localhost:8000/ws"

# WebSocket 认证配置
WS_AUTH_ENABLED = os.getenv("WEBSOCKET_AUTH_ENABLED", "false").lower() in ("true", "1", "yes")
WS_AUTH_TOKEN = os.getenv("WEBSOCKET_AUTH_TOKEN", "")