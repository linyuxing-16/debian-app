from PyQt5.QtCore import QObject,pyqtSignal

class Receiver(QObject):
    signal = pyqtSignal(str,str)
