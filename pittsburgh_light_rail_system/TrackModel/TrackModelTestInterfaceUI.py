import sys
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

class TestUI(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model - Test Interface')
        self.left = 650
        self.top = 10
        self.width = 640
        self.height = 540
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout = QVBoxLayout()
        
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)