from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QPushButton, QGraphicsDropShadowEffect, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import queue
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import io
import base64
import threading
import json

class textarea(QWidget):
    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.ws_client = None
        self.is_recording = False
        self.audio_data = None
        self.record_thread = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(624, 80)
        self._drag_position = None

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.gray)
        shadow.setOffset(0, 5)

        self.main_widget = QWidget(self)
        self.main_widget.setGeometry(0, 0, 624, 80)
        self.main_widget.setGraphicsEffect(shadow)
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 255),
                    stop:1 rgba(240, 240, 240, 255));
                border-radius: 10px;
                border: 2px solid rgba(200, 200, 200, 100);
            }
        """)

        # 外层垂直布局
        self.outer_layout = QVBoxLayout(self.main_widget)
        self.outer_layout.setContentsMargins(15, 5, 15, 5)
        self.outer_layout.setSpacing(2)
        self.setLayout(self.outer_layout)

        # 输入行水平布局
        self.input_layout = QHBoxLayout()

        self.textarea = QTextEdit()
        self.textarea.setFixedSize(480, 35)
        self.textarea.setPlaceholderText("请输入文本")
        self.textarea.setFont(QFont("微软雅黑", 10))
        self.textarea.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 255);
                border: 1px solid rgba(200, 200, 200, 150);
                border-radius: 8px;
                padding: 5px 10px;
                color: #000;
            }
            QTextEdit:focus {
                background-color: rgba(255, 255, 255, 255);
                border: 2px solid rgba(0, 0, 0, 100);
            }
        """)
        self.input_layout.addWidget(self.textarea)

        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send)
        self.send_button.setFixedSize(80, 35)
        self.send_button.setFont(QFont("微软雅黑", 10))
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 80);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 60);
            }
        """)
        self.input_layout.addWidget(self.send_button)

        # 录音按钮
        self.record_button = QPushButton("录音")
        self.record_button.clicked.connect(self.toggle_record)
        self.record_button.setFixedSize(60, 35)
        self.record_button.setFont(QFont("微软雅黑", 9))
        self.record_button.setCursor(Qt.PointingHandCursor)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 80);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 60);
            }
        """)
        self.input_layout.addWidget(self.record_button)

        self.close_button = QPushButton("×")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedSize(25, 25)
        self.close_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 100, 100, 200);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 230);
            }
            QPushButton:pressed {
                background-color: rgba(255, 60, 60, 200);
            }
        """)
        self.input_layout.addWidget(self.close_button)

        self.outer_layout.addLayout(self.input_layout)

        # 状态标签
        self.status_label = QLabel("连接中...")
        self.status_label.setFont(QFont("微软雅黑", 8))
        self.status_label.setStyleSheet("color: gray; padding-left: 5px;")
        self.outer_layout.addWidget(self.status_label)

        self.main_widget.mouseMoveEvent = self.mouseMoveEvent
        self.main_widget.mousePressEvent = self.mousePressEvent
        self.main_widget.mouseReleaseEvent = self.mouseReleaseEvent

    def getText(self):
        return self.textarea.toPlainText()

    def send(self):
        self.q.put(self.getText())
        self.textarea.clear()

    def get_message(self):
        return self.q.get()

    def set_websocket_client(self, ws_client):
        """设置 WebSocket 客户端引用"""
        self.ws_client = ws_client

    def update_connection_status(self):
        """更新连接状态显示"""
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

    def toggle_record(self):
        """切换录音状态"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """开始录音"""
        self.is_recording = True
        self.record_button.setText("停止")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(220, 53, 69, 200);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(200, 35, 51, 230);
            }
            QPushButton:pressed {
                background-color: rgba(180, 30, 45, 200);
            }
        """)
        self.status_label.setText("录音中...")
        self.status_label.setStyleSheet("color: #DC3545; padding-left: 5px;")
        self.record_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.record_thread.start()

    def _record_audio(self):
        """后台录音线程"""
        try:
            self.audio_data = sd.rec(int(44100 * 60), samplerate=44100, channels=1, dtype=np.int16)
            sd.wait()
        except Exception as e:
            print(f"录音错误: {e}")
            self.is_recording = False

    def stop_recording(self):
        """停止录音并发送"""
        self.is_recording = False
        sd.stop()
        self.record_button.setText("录音")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 80);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 60);
            }
        """)
        self._send_audio()

    def _send_audio(self):
        """将录音编码为 Base64 WAV 并发送"""
        if self.audio_data is None or len(self.audio_data) == 0:
            return

        try:
            # 找到实际录音长度（去除静音尾部）
            audio_array = self.audio_data.flatten()

            # 转换为 WAV 格式
            buffer = io.BytesIO()
            wavfile.write(buffer, 44100, audio_array)
            wav_data = buffer.getvalue()

            # Base64 编码
            base64_audio = base64.b64encode(wav_data).decode('utf-8')

            # 构造消息
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
        except Exception as e:
            print(f"发送音频错误: {e}")
            self.status_label.setText("发送失败")
            self.status_label.setStyleSheet("color: #F44336; padding-left: 5px;")

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    window = textarea() 
    window.show()
    sys.exit(app.exec())
        
