import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

# 默认值
DEFAULT_WS_URL = "ws://localhost:8000/ws"
DEFAULT_AUTH_ENABLED = False
DEFAULT_AUTH_TOKEN = ""


def load_config():
    """从 JSON 文件加载配置，不存在则返回默认值"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_config(config):
    """保存配置到 JSON 文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


# 初始化配置
_config = load_config()
WS_URL = _config.get("ws_url", DEFAULT_WS_URL)
WS_AUTH_ENABLED = _config.get("auth_enabled", DEFAULT_AUTH_ENABLED)
WS_AUTH_TOKEN = _config.get("auth_token", DEFAULT_AUTH_TOKEN)


def update_config(ws_url=None, auth_enabled=None, auth_token=None):
    """更新配置并持久化到文件"""
    global WS_URL, WS_AUTH_ENABLED, WS_AUTH_TOKEN
    if ws_url is not None:
        WS_URL = ws_url
    if auth_enabled is not None:
        WS_AUTH_ENABLED = auth_enabled
    if auth_token is not None:
        WS_AUTH_TOKEN = auth_token
    save_config({
        "ws_url": WS_URL,
        "auth_enabled": WS_AUTH_ENABLED,
        "auth_token": WS_AUTH_TOKEN
    })
