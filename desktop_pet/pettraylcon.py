from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon


class Traylcon(QSystemTrayIcon):
    def __init__(self, pet_window, chat_window, textarea_window, parent=None):
        super().__init__(parent)
        self.pet_window = pet_window
        self.chat_window = chat_window
        self.textarea_window = textarea_window

        self.setIcon(QIcon("desktop_pet/pet-png/calm.png"))

        menu = QMenu()

        self.pet_action = QAction("宠物窗口", self, checkable=True)
        self.pet_action.setChecked(True)
        self.pet_action.triggered.connect(self.toggle_pet)
        menu.addAction(self.pet_action)

        self.chat_action = QAction("聊天窗口", self, checkable=True)
        self.chat_action.setChecked(True)
        self.chat_action.triggered.connect(self.toggle_chat)
        menu.addAction(self.chat_action)

        self.textarea_action = QAction("输入框", self, checkable=True)
        self.textarea_action.setChecked(True)
        self.textarea_action.triggered.connect(self.toggle_textarea)
        menu.addAction(self.textarea_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def toggle_pet(self):
        if self.pet_action.isChecked():
            self.pet_window.show()
        else:
            self.pet_window.hide()

    def toggle_chat(self):
        if self.chat_action.isChecked():
            self.chat_window.show()
        else:
            self.chat_window.hide()

    def toggle_textarea(self):
        if self.textarea_action.isChecked():
            self.textarea_window.show()
        else:
            self.textarea_window.hide()

    def quit_app(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
