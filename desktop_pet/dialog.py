from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QCheckBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QBrush, QColor
import queue
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import io
import base64
import threading
import json
import config


class DialogWindow(QWidget):
    """统一的对话框窗口，包含输入和显示功能"""

    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.ws_client = None
        self.is_recording = False
        self.audio_data = None
        self.record_thread = None

        # 窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(config.DIALOG_WIDTH, config.DIALOG_HEIGHT)
        self.setWindowOpacity(0.95)

        # 拖动相关
        self._drag_position = None

        # 主布局
        self._setup_ui()

    def _setup_ui(self):
        """设置 UI 布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 10)
        main_layout.setSpacing(2)

        # 顶部：角色名称标签
        self.name_label = QLabel("你")
        self.name_label.setFont(QFont("Microsoft YaHei", 14))
        self.name_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(self.name_label)

        # 中间：文本区域 + 滚动条
        text_layout = QHBoxLayout()
        text_layout.setSpacing(0)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Microsoft YaHei", 14))
        self.text_edit.setPlaceholderText("说点什么吧（Shift+Enter换行 Enter发送）")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                color: black;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: transparent;
                width: 8px;
                height: 8px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: rgba(136, 136, 136, 0.5);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: rgba(136, 136, 136, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: transparent;
                border: none;
                height: 0px;
                width: 0px;
            }
        """)
        self.text_edit.setFrameShape(QTextEdit.NoFrame)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.keyPressEvent = self._key_press_event

        text_layout.addWidget(self.text_edit)

        # 自定义滚动条
        self.scroll_bar = QLabel()
        self.scroll_bar.setFixedWidth(8)
        self.scroll_bar.setStyleSheet("""
            background: rgba(136, 136, 136, 0.3);
            border-radius: 4px;
        """)
        self.scroll_bar.hide()
        text_layout.addWidget(self.scroll_bar)

        main_layout.addLayout(text_layout)

        # 底部：按钮行
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        # 麦克风按钮
        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(35, 30)
        self.mic_button.setFont(QFont("Arial", 12))
        self.mic_button.setCursor(Qt.PointingHandCursor)
        self.mic_button.clicked.connect(self._toggle_record)
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                color: black;
            }
            QPushButton:hover {
                border: 2px solid #CCCCCC;
            }
            QPushButton:pressed {
                border: 2px solid #AAAAAA;
                background-color: rgba(220, 53, 69, 100);
            }
        """)
        button_layout.addWidget(self.mic_button)

        # 直接发送复选框
        self.auto_send_checkbox = QCheckBox("直接发送")
        self.auto_send_checkbox.setFont(QFont("Microsoft YaHei", 10))
        self.auto_send_checkbox.setToolTip("语音识别完成后将会直接发送")
        self.auto_send_checkbox.setStyleSheet("""
            QCheckBox {
                background-color: transparent;
                border: none;
                padding: 5px 10px;
                color: black;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #CCCCCC;
                background-color: #CCCCCC;
                border-radius: 5px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #BBBBBB;
                background-color: transparent;
                border-radius: 5px;
            }
        """)
        button_layout.addWidget(self.auto_send_checkbox)

        # 弹簧
        button_layout.addStretch()

        # 状态标签
        self.status_label = QLabel("连接中...")
        self.status_label.setFont(QFont("Microsoft YaHei", 8))
        self.status_label.setStyleSheet("color: gray; padding-left: 5px;")
        button_layout.addWidget(self.status_label)

        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def paintEvent(self, event):
        """绘制圆角背景和阴影"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 绘制阴影
        for i in range(5):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
            rect = QRectF(5 - i, 5 - i, self.width() - (5 - i) * 2, self.height() - (5 - i) * 2)
            path.addRoundedRect(rect, 15, 15)
            color = QColor(0, 0, 0, 50 - int(i ** 0.5 * 22))
            painter.setPen(color)
            painter.drawPath(path)

        # 绘制白色圆角背景
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        rect = QRectF(5, 5, self.width() - 10, self.height() - 10)
        path.addRoundedRect(rect, 15, 15)
        painter.fillPath(path, QBrush(Qt.white))

    def _key_press_event(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() & Qt.ShiftModifier:
                # Shift+Enter 换行
                self.text_edit.insertPlainText("\n")
            else:
                # Enter 发送
                self._send()
        else:
            # 其他按键正常处理
            QTextEdit.keyPressEvent(self.text_edit, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_position is not None:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = None
            event.accept()

    # ========== 发送功能 ==========

    def getText(self):
        return self.text_edit.toPlainText()

    def _send(self):
        text = self.getText()
        if text.strip():
            self.q.put(text)
            self.text_edit.clear()

    def get_message(self):
        return self.q.get()

    # ========== WebSocket 状态 ==========

    def set_websocket_client(self, ws_client):
        self.ws_client = ws_client

    def update_connection_status(self):
        if self.ws_client is None:
            return
        if self.ws_client.is_connected():
            self.status_label.setText("已连接")
            self.status_label.setStyleSheet("color: #4CAF50; padding-left: 5px;")
        elif self.ws_client._connecting:
            self.status_label.setText("连接中...")
            self.status_label.setStyleSheet("color: gray; padding-left: 5px;")
        else:
            self.status_label.setText("未连接")
            self.status_label.setStyleSheet("color: #F44336; padding-left: 5px;")

    # ========== 消息显示 ==========

    def chat(self, message, msg_type):
        """接收消息并显示（API 逐字发送，直接累积显示）"""
        if msg_type == "event":
            # 重置状态，准备下一轮对话
            self._set_mode("input")
            self.name_label.setText("你")
            self.text_edit.clear()
            self.text_edit.setEnabled(True)
        elif msg_type in ("type", "reasoning"):
            # API 逐字发送，直接累积显示
            self.name_label.setText("AI")
            self._set_mode("display")
            self.text_edit.setText(message)

    def _set_mode(self, mode):
        """切换输入/显示模式"""
        if mode == "input":
            self.text_edit.setEnabled(True)
            self.text_edit.setPlaceholderText("说点什么吧（Shift+Enter换行 Enter发送）")
        elif mode == "display":
            self.text_edit.setEnabled(False)
            self.text_edit.setPlaceholderText("")

    # ========== 录音功能 ==========

    def _toggle_record(self):
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.is_recording = True
        self.mic_button.setText("🔴")
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(220, 53, 69, 200);
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(200, 35, 51, 230);
            }
        """)
        self.status_label.setText("录音中...")
        self.status_label.setStyleSheet("color: #DC3545; padding-left: 5px;")
        self.record_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.record_thread.start()

    def _record_audio(self):
        try:
            self.audio_data = sd.rec(int(44100 * 60), samplerate=44100, channels=1, dtype=np.int16)
            sd.wait()
        except Exception as e:
            print(f"录音错误: {e}")
            self.is_recording = False

    def _stop_recording(self):
        self.is_recording = False
        sd.stop()
        self.mic_button.setText("🎤")
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                color: black;
            }
            QPushButton:hover {
                border: 2px solid #CCCCCC;
            }
            QPushButton:pressed {
                border: 2px solid #AAAAAA;
                background-color: rgba(220, 53, 69, 100);
            }
        """)
        self._send_audio()

    def _send_audio(self):
        if self.audio_data is None or len(self.audio_data) == 0:
            return

        try:
            audio_array = self.audio_data.flatten()
            buffer = io.BytesIO()
            wavfile.write(buffer, 44100, audio_array)
            wav_data = buffer.getvalue()
            base64_audio = base64.b64encode(wav_data).decode('utf-8')

            message = json.dumps({
                "attachments": [{
                    "type": "audio",
                    "url": f"data:audio/wav;base64,{base64_audio}",
                    "format": "wav"
                }]
            })

            self.q.put(message)
            self.status_label.setText("已发送")
            self.status_label.setStyleSheet("color: #4CAF50; padding-left: 5px;")

            if self.auto_send_checkbox.isChecked():
                # 自动发送模式，直接发送文本
                pass

        except Exception as e:
            print(f"发送音频错误: {e}")
            self.status_label.setText("发送失败")
            self.status_label.setStyleSheet("color: #F44336; padding-left: 5px;")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DialogWindow()
    window.show()
    sys.exit(app.exec())