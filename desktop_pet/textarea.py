from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import queue

class textarea(QWidget):
    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(624, 60)
        self._drag_position = None
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.gray)
        shadow.setOffset(0, 5)
        
        self.main_widget = QWidget(self)
        self.main_widget.setGeometry(0, 0, 624, 60)
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
        
        self.layout = QHBoxLayout(self.main_widget)
        self.layout.setContentsMargins(15, 10, 15, 10)
        self.setLayout(self.layout)
        
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
        self.layout.addWidget(self.textarea)
        
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
        self.layout.addWidget(self.send_button)
        
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
        self.layout.addWidget(self.close_button)
        
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
        
