from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox, QSpinBox
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QBrush, QColor
import config


class SettingsWindow(QWidget):
    """设置窗口"""

    def __init__(self):
        super().__init__()
        self._drag_position = None

        # 窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 420)
        self.setWindowOpacity(0.95)
        self.setWindowTitle("设置")

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """设置 UI 布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        # 标题
        title_label = QLabel("设置")
        title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(title_label)

        # WebSocket URL
        url_label = QLabel("WebSocket 服务器地址")
        url_label.setFont(QFont("Microsoft YaHei", 10))
        url_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setFont(QFont("Microsoft YaHei", 10))
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        main_layout.addWidget(self.url_input)

        # 启用认证
        self.auth_checkbox = QCheckBox("启用 Token 认证")
        self.auth_checkbox.setFont(QFont("Microsoft YaHei", 10))
        self.auth_checkbox.setStyleSheet("""
            QCheckBox {
                background-color: transparent;
                color: black;
                padding: 5px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #CCCCCC;
                background-color: transparent;
                border-radius: 4px;
            }
        """)
        main_layout.addWidget(self.auth_checkbox)

        # Auth Token
        token_label = QLabel("认证 Token")
        token_label.setFont(QFont("Microsoft YaHei", 10))
        token_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(token_label)

        self.token_input = QLineEdit()
        self.token_input.setFont(QFont("Microsoft YaHei", 10))
        self.token_input.setEchoMode(QLineEdit.Password)
        self.token_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        main_layout.addWidget(self.token_input)

        # 分隔线
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #CCCCCC;")
        main_layout.addWidget(separator)

        # 宠物窗口大小设置
        pet_size_label = QLabel("宠物窗口大小")
        pet_size_label.setFont(QFont("Microsoft YaHei", 10))
        pet_size_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(pet_size_label)

        pet_size_layout = QHBoxLayout()
        pet_size_layout.setSpacing(10)

        pet_width_label = QLabel("宽度:")
        pet_width_label.setFont(QFont("Microsoft YaHei", 9))
        pet_width_label.setStyleSheet("color: black; background: transparent;")
        pet_size_layout.addWidget(pet_width_label)

        self.pet_width_spin = QSpinBox()
        self.pet_width_spin.setRange(100, 400)
        self.pet_width_spin.setSuffix(" px")
        self.pet_width_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 3px 5px;
                color: black;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        pet_size_layout.addWidget(self.pet_width_spin)

        pet_height_label = QLabel("高度:")
        pet_height_label.setFont(QFont("Microsoft YaHei", 9))
        pet_height_label.setStyleSheet("color: black; background: transparent;")
        pet_size_layout.addWidget(pet_height_label)

        self.pet_height_spin = QSpinBox()
        self.pet_height_spin.setRange(150, 500)
        self.pet_height_spin.setSuffix(" px")
        self.pet_height_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 3px 5px;
                color: black;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        pet_size_layout.addWidget(self.pet_height_spin)
        pet_size_layout.addStretch()

        main_layout.addLayout(pet_size_layout)

        # 对话框窗口大小设置
        dialog_size_label = QLabel("对话框窗口大小")
        dialog_size_label.setFont(QFont("Microsoft YaHei", 10))
        dialog_size_label.setStyleSheet("color: black; background: transparent;")
        main_layout.addWidget(dialog_size_label)

        dialog_size_layout = QHBoxLayout()
        dialog_size_layout.setSpacing(10)

        dialog_width_label = QLabel("宽度:")
        dialog_width_label.setFont(QFont("Microsoft YaHei", 9))
        dialog_width_label.setStyleSheet("color: black; background: transparent;")
        dialog_size_layout.addWidget(dialog_width_label)

        self.dialog_width_spin = QSpinBox()
        self.dialog_width_spin.setRange(400, 1000)
        self.dialog_width_spin.setSuffix(" px")
        self.dialog_width_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 3px 5px;
                color: black;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        dialog_size_layout.addWidget(self.dialog_width_spin)

        dialog_height_label = QLabel("高度:")
        dialog_height_label.setFont(QFont("Microsoft YaHei", 9))
        dialog_height_label.setStyleSheet("color: black; background: transparent;")
        dialog_size_layout.addWidget(dialog_height_label)

        self.dialog_height_spin = QSpinBox()
        self.dialog_height_spin.setRange(100, 400)
        self.dialog_height_spin.setSuffix(" px")
        self.dialog_height_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 3px 5px;
                color: black;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
            }
        """)
        dialog_size_layout.addWidget(self.dialog_height_spin)
        dialog_size_layout.addStretch()

        main_layout.addLayout(dialog_size_layout)

        # 按钮行
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        save_button = QPushButton("保存")
        save_button.setFont(QFont("Microsoft YaHei", 10))
        save_button.setFixedSize(80, 30)
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self._save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("取消")
        cancel_button.setFont(QFont("Microsoft YaHei", 10))
        cancel_button.setFixedSize(80, 30)
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.close)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        button_layout.addWidget(cancel_button)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_position is not None:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = None
            event.accept()

    def _load_settings(self):
        """加载当前配置"""
        self.url_input.setText(config.WS_URL)
        self.auth_checkbox.setChecked(config.WS_AUTH_ENABLED)
        self.token_input.setText(config.WS_AUTH_TOKEN)
        self.pet_width_spin.setValue(config.PET_WIDTH)
        self.pet_height_spin.setValue(config.PET_HEIGHT)
        self.dialog_width_spin.setValue(config.DIALOG_WIDTH)
        self.dialog_height_spin.setValue(config.DIALOG_HEIGHT)

    def _save_settings(self):
        """保存设置"""
        ws_url = self.url_input.text().strip()
        auth_enabled = self.auth_checkbox.isChecked()
        auth_token = self.token_input.text().strip()
        pet_width = self.pet_width_spin.value()
        pet_height = self.pet_height_spin.value()
        dialog_width = self.dialog_width_spin.value()
        dialog_height = self.dialog_height_spin.value()

        if not ws_url:
            QMessageBox.warning(self, "警告", "WebSocket 地址不能为空")
            return

        config.update_config(
            ws_url=ws_url,
            auth_enabled=auth_enabled,
            auth_token=auth_token,
            pet_width=pet_width,
            pet_height=pet_height,
            dialog_width=dialog_width,
            dialog_height=dialog_height
        )
        QMessageBox.information(self, "成功", "设置已保存，重启应用后生效")
        self.close()