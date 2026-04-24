# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

桌面宠物（桌宠）应用，使用 PyQt5 连接 WebSocket 服务器进行 AI 聊天交互。宠物根据消息类型显示不同表情。

## 运行应用

```bash
source .venv/bin/activate
python desktop_pet/main.py
```

WebSocket 认证环境变量：
- `WEBSOCKET_AUTH_ENABLED=true` - 启用 token 认证
- `WEBSOCKET_AUTH_TOKEN=your_token` - 认证 token 值

## 架构

### 三窗口 UI 系统
- **pet_ui.py** - 宠物精灵窗口（200x300，无边框透明，可拖拽）。从 `desktop_pet/pet-png/` 目录加载 PNG 图片
- **chat_ui.py** - 聊天气泡窗口（400x150，圆角渐变）。显示 AI 回复文本
- **textarea.py** - 输入组件（624x60）。文本输入框和发送按钮

### 消息流程
```
应用启动 → 显示 UI → 后台异步连接 WebSocket
                                    ↓
用户输入 → textarea → websocket_class → WebSocket 服务器
                                      ↓
WebSocket 服务器 → receive_message → JSON 解析 → PyQt Signal → UI 更新
```

**注意**: WebSocket 连接在后台异步进行，服务器不可用时应用也能正常启动。

### 核心组件
- **main.py**: 入口点。先显示 UI 窗口，再异步连接 WebSocket，启动 `receive_message` 和 `send_message` 守护线程
- **websocket_class.py**: 基于队列的消息缓冲 WebSocket 客户端，支持异步连接和自动重连
- **base.py**: `Receiver` QObject，包含跨线程通信用的 `pyqtSignal(str, str)`
- **config.py**: WebSocket URL（`ws://localhost:8000/ws`）和认证配置
- **pettraylcon.py**: 系统托盘图标，提供菜单控制三个窗口的显示/隐藏和退出应用

### 表情状态（pet_ui.py）
- `resetExpression()` → `calm.png`
- `startTalking()` → `talk.png`
- `startThinking()` → `think.png`

### 消息类型（main.py）
- `type: "reasoning"` - 触发说话动画，内容不累积
- `type: "message"` - 累积文本内容，触发动画
- `event: 任意` - 重置累积内容和宠物表情

## 资源文件要求

需在 `desktop_pet/pet-png/` 目录放置 PNG 文件：
- `calm.png` - 默认/待机表情
- `talk.png` - 说话动画帧
- `think.png` - 思考动画帧

目前只有 `calm.png` 和 `pet.avif`，其他资源需补充。

## 依赖

```
PyQt5>=5.15.9
websocket-client>=1.0.0
pystray>=0.19.0
Pillow>=9.0.0
```
