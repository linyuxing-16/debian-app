# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 PyQt5 的桌面宠物应用。屏幕上显示可拖动的宠物角色，配合对话框窗口通过 WebSocket 进行 AI 聊天交互。包含系统托盘集成、设置管理和语音录制功能。

## 常用命令

```bash
# 安装依赖
pip install -r desktop_pet/requirements.txt

# 运行应用
cd /home/linyuxin/Desktop/app/debian-app && python desktop_pet/main.py
```

## 架构

```
desktop_pet/
├── main.py           # 应用入口，协调所有组件
├── config.py         # 配置管理（JSON 持久化）
├── websocket_class.py # WebSocket 客户端，支持自动重连和 Token 认证
├── base.py           # Qt 信号发射器，用于跨线程通信
├── pet_ui.py         # 可拖动的宠物窗口，包含表情状态和右键菜单
├── dialog.py         # 统一的对话框窗口，支持文本输入、消息显示和语音录制
├── settings_ui.py    # 设置窗口，配置 WebSocket 和 UI 参数
├── pettraylcon.py    # 系统托盘图标及右键菜单
├── config.json       # 运行时配置文件
└── pet-png/          # 宠物图片（calm.png, talk.png, think.png）
```

### 核心设计

- **线程模型**：两个守护线程处理 WebSocket I/O（`receive_message`、`send_message`）。UI 更新通过 `base.py` 中的 `Receiver` 类使用 Qt 信号机制，确保线程安全。
- **配置系统**：`config.py` 提供全局设置和 JSON 持久化。窗口尺寸和 WebSocket 设置可通过 `settings_ui.py` 运行时配置，保存后重启生效。
- **消息协议**：WebSocket 消息为 JSON 格式。类型包括：
  - `reasoning`：AI 思考状态，触发宠物说话动画
  - `message`：文本内容，支持字符串或内容对象列表
  - `event`：对话重置事件
- **语音录制**：`dialog.py` 使用 `sounddevice` 捕获音频，转换为 WAV 格式，编码为 base64 后通过 WebSocket 发送。支持"直接发送"选项。
- **认证机制**：WebSocket 支持可选的 Token 认证，通过 URL 参数传递。

### UI 组件

- **宠物窗口**：无边框、透明背景、可拖动。右键菜单提供对话框切换、设置和退出功能。
- **对话框窗口**：统一的输入/显示组件。Enter 发送消息，Shift+Enter 换行。显示 AI 回复时点击可重置为输入模式。
- **设置窗口**：配置 WebSocket 地址、Token 认证、宠物和对话框窗口尺寸。
- **系统托盘**：快速切换宠物窗口和对话框的显示/隐藏，访问设置。

### 依赖

- PyQt5 >= 5.15.9：UI 框架
- websocket-client >= 1.0.0：WebSocket 通信
- sounddevice：音频录制
- numpy + scipy：音频数据处理
