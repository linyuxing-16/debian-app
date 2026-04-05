# WebSocket 通道 API 消息模型

## 概述

WebSocket 通道通过 WebSocket 协议接收客户端消息。服务器默认监听 `127.0.0.1:8765`。

## 连接地址

```
ws://<host>:<port>[?token=<token>]
```

默认配置：`ws://127.0.0.1:8765`

**注意**：如果启用了身份验证，连接时必须提供有效的 token。

---

## 身份验证

WebSocket 通道支持可选的 Bearer Token 身份验证。

### 认证方式

#### 1. Query 参数（推荐）

```
ws://127.0.0.1:8765?token=my_secret_token
```

#### 2. Authorization Header

```
Authorization: Bearer my_secret_token
# 或
Authorization: Token my_secret_token
```

### 认证失败

如果提供的 token 无效或缺失，服务器将关闭 WebSocket 连接：

| Code | Reason | 说明 |
|------|--------|------|
| `1008` | `Authentication required` | Token 无效或缺失 |

### 启用认证

通过环境变量启用：

```bash
export WEBSOCKET_AUTH_ENABLED=1
export WEBSOCKET_AUTH_TOKEN=my_secret_token
```

---

## 消息格式

### 请求消息（客户端 → 服务器）

客户端发送的消息应为 JSON 格式：

```json
{
  "text": "消息文本内容",
  "channel_id": "可选，渠道标识",
  "sender_id": "可选，发送者标识",
  "session_id": "可选，会话标识",
  "meta": {},
  "attachments": []
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | **是** | 消息文本内容 |
| `channel_id` | string | 否 | 渠道标识，默认为 "websocket" |
| `sender_id` | string | 否 | 发送者标识，会被自动覆盖为客户端地址 |
| `session_id` | string | 否 | 会话标识，用于关联对话 |
| `meta` | object | 否 | 附加元数据，会传递给 agent |
| `attachments` | array | 否 | 附件列表 |
| `bot_prefix` | string | 否 | 机器人回复前缀 |

### 过滤器参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `filter_tool_messages` | bool | `false` | 过滤工具调用消息 |
| `filter_thinking` | bool | `false` | 过滤思考过程 |

### 附件格式 (attachments)

每个附件对象支持以下字段：

```json
{
  "type": "image|video|audio|file",
  "url": "https://example.com/path/to/file",
  "data": "https://example.com/path/to/audio.mp3",
  "format": "mp3",
  "filename": "example.mp3"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | **是** | 附件类型：`image`、`video`、`audio`、`file` |
| `url` | string | **是** | 文件访问 URL（`image`、`video`、`file` 类型使用） |
| `data` | string | **是** | 文件访问 URL（`audio` 类型使用） |
| `format` | string | 否 | 音频格式（如 `mp3`、`wav`），仅 `audio` 类型需要 |
| `filename` | string | 否 | 文件名，仅 `file` 类型需要 |

---

## 示例

### 文本消息

```json
{
  "text": "你好，请帮我分析这个问题"
}
```

### 带附件的消息

```json
{
  "text": "请查看这张图片",
  "attachments": [
    {
      "type": "image",
      "url": "https://example.com/screenshot.png"
    }
  ]
}
```

### 完整参数示例

```json
{
  "text": "请处理这个音频文件",
  "channel_id": "websocket",
  "session_id": "user-123-session-456",
  "meta": {
    "priority": "high",
    "source": "mobile-app"
  },
  "attachments": [
    {
      "type": "audio",
      "data": "https://example.com/voice.mp3",
      "format": "mp3"
    }
  ]
}
```

### 非 JSON 消息

如果客户端发送的不是有效 JSON，服务器会自动包装为：

```json
{
  "text": "<原始消息内容>"
}
```

---

## 响应消息

服务器通过 WebSocket 发送流式响应，使用 SSE（Server-Sent Events）格式。

### 流式响应格式

```
data: {"type": "text", "content": "回复内容片段1"}\n\n
data: {"type": "text", "content": "回复内容片段2"}\n\n
data: {"event": "finish", "content": ""}\n\n
```

### 响应事件类型

| 事件类型 | 说明 |
|----------|------|
| `text` | 文本内容片段 |
| `finish` | 流式输出结束标记 |
| `error` | 错误信息 |

响应内容为 JSON 格式，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 事件类型 |
| `content` | string | 内容片段 |
| `bot_prefix` | string | 机器人前缀（如配置） |

---

## 配置参数

通过环境变量或配置文件设置：

| 参数 | 环境变量 | 默认值 | 说明 |
|------|----------|--------|------|
| `host` | `WEBSOCKET_HOST` | `127.0.0.1` | 监听地址 |
| `port` | `WEBSOCKET_PORT` | `8765` | 监听端口 |
| `bot_prefix` | `WEBSOCKET_BOT_PREFIX` | `""` | 机器人回复前缀 |
| `auth_enabled` | `WEBSOCKET_AUTH_ENABLED` | `false` | 是否启用身份验证 |
| `auth_token` | `WEBSOCKET_AUTH_TOKEN` | `""` | Bearer token 值 |
| `filter_tool_messages` | - | `false` | 过滤工具调用消息（仅支持代码配置） |
| `filter_thinking` | - | `false` | 过滤思考过程（仅支持代码配置） |
