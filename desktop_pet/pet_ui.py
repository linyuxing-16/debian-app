from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QVBoxLayout,QMenu,QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import config

class pet_window(QWidget):
    def __init__(self, dialog_window=None, settings_window=None):
        super().__init__()
        self.dialog_window = dialog_window
        self.settings_window = settings_window
        self.setWindowTitle("桌面宠物")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QLabel()
        self.label.setFixedSize(config.PET_WIDTH, config.PET_HEIGHT)
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

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # 显示/隐藏对话框
        dialog_action = QAction("对话框", self, checkable=True)
        if self.dialog_window:
            dialog_action.setChecked(self.dialog_window.isVisible())
        dialog_action.triggered.connect(self.toggle_dialog)
        menu.addAction(dialog_action)

        menu.addSeparator()

        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)

        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        menu.exec_(event.globalPos())

    def toggle_dialog(self):
        if self.dialog_window:
            if self.dialog_window.isVisible():
                self.dialog_window.hide()
            else:
                self.dialog_window.show()

    def show_settings(self):
        if self.settings_window:
            self.settings_window.show()

    def quit_app(self):
        QApplication.quit()

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
