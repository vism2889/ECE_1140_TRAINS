from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class signalSender(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

        self.occupancy = [True, False, True, False]

        self.pb = QPushButton("EMIT", self)
        self.pb.setGeometry(125, 100, 150, 50)
        self.pb.clicked.connect(self.emit)
        self.setWindowTitle("Signal Sender")
        self.setGeometry(100, 100, 400, 600)
        
        self.show()
    
    def emit(self):
        print("Emitting From Signal Sender")
        self.signals.occupancySignal.emit(self.occupancy)
