from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
import sys

class pet_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("桌面宠物")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QLabel()
        self.label.setFixedSize(200, 300)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)
        self.resetExpression()
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = None
            event.accept()

    def resetExpression(self):
        "将宠物的图片设置为默认图片"
        self.label.setPixmap(QPixmap("desktop_pet/pet-png/calm.png"))

    def startTalking(self):
        "将图片设置为说话图片"
        self.label.setPixmap(QPixmap("desktop_pet/pet-png/talk.png"))

    def startThinking(self):
        "将图片设置为思考图片"
        self.label.setPixmap(QPixmap("desktop_pet/pet-png/think.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pet_window()
    window.show()
    sys.exit(app.exec())
