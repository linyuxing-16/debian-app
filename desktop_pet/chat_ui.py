from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
import sys

class pet_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 150)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.gray)
        shadow.setOffset(0, 5)
        
        main_widget = QWidget(self)
        main_widget.setGeometry(0, 0, 400, 150)
        main_widget.setGraphicsEffect(shadow)
        main_widget.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(85, 170, 255, 240), 
                    stop:1 rgba(135, 206, 250, 250));
                border-radius: 10px;
                border: 2px solid rgba(255, 255, 255, 100);
            }
        """)
        
        title_bar = QWidget(main_widget)
        title_bar.setGeometry(0, 0, 400, 35)
        title_bar.setStyleSheet("background-color: transparent;")
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        title_label = QLabel("桌面宠物 ✨")
        title_label.setFont(QFont("微软雅黑", 10, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent;")
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.min_btn = QPushButton("−")
        self.min_btn.setFixedSize(30, 25)
        self.min_btn.clicked.connect(self.showMinimized)
        
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(30, 25)
        self.max_btn.clicked.connect(self.toggle_maximize)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 25)
        self.close_btn.clicked.connect(self.close)
        
        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFont(QFont("Arial", 12))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 150);
                    border: none;
                    border-radius: 5px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 200);
                }
            """)
        
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 100, 100, 200);
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 230);
            }
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.max_btn)
        title_layout.addWidget(self.close_btn)
        
        self.layout = QVBoxLayout(main_widget)
        self.layout.setContentsMargins(20, 50, 20, 20)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("微软雅黑", 11))
        self.label.setStyleSheet("color: white; background: transparent;")
        self.layout.addWidget(self.label)
        
        self.drag_position = None
        title_bar.mousePressEvent = self.mouse_press
        title_bar.mouseMoveEvent = self.mouse_move

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("❐")

    def chat(self, send_msg):
        self.label.setText(send_msg)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pet_window()
    window.chat("你好")
    window.show()
    sys.exit(app.exec())