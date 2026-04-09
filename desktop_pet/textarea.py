from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout,QTextEdit,QPushButton
import queue

class textarea(QWidget):
    def __init__(self,q:queue.Queue):
        super().__init__()
        self.q = q
        self.setWindowTitle("桌面宠物")
        self.setFixedSize(624, 50)
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.textarea = QTextEdit()
        self.textarea.setFixedSize(500, 30)
        self.textarea.setPlaceholderText("请输入文本")
        self.layout.addWidget(self.textarea)
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send)
        self.send_button.setFixedSize(100, 30)
        self.layout.addWidget(self.send_button)

    def getText(self):
        return self.textarea.toPlainText()

    def send(self):
        self.q.put(self.getText())
        self.textarea.clear()

    def get_q(self):
        return self.q

if __name__ == "__main__":
    import sys
    import threading
    app = QApplication(sys.argv)
    q = queue.Queue()
    window = textarea(q)
    window.show()
    def print_q():
        while True:
            print(q.get())
    t = threading.Thread(target=print_q)
    t.start()
    
    sys.exit(app.exec())
        
