from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon


class Traylcon(QSystemTrayIcon):
    def __init__(self, pet_window, dialog_window, settings_window, parent=None):
        super().__init__(parent)
        self.pet_window = pet_window
        self.dialog_window = dialog_window
        self.settings_window = settings_window

        self.setIcon(QIcon("desktop_pet/pet-png/calm.png"))

        menu = QMenu()

        self.pet_action = QAction("宠物窗口", self, checkable=True)
        self.pet_action.setChecked(True)
        self.pet_action.triggered.connect(self.toggle_pet)
        menu.addAction(self.pet_action)

        self.dialog_action = QAction("对话框", self, checkable=True)
        self.dialog_action.setChecked(True)
        self.dialog_action.triggered.connect(self.toggle_dialog)
        menu.addAction(self.dialog_action)

        menu.addSeparator()

        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def toggle_pet(self):
        if self.pet_action.isChecked():
            self.pet_window.show()
        else:
            self.pet_window.hide()

    def toggle_dialog(self):
        if self.dialog_action.isChecked():
            self.dialog_window.show()
        else:
            self.dialog_window.hide()

    def show_settings(self):
        self.settings_window.show()
        self.settings_window.activateWindow()

    def quit_app(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()