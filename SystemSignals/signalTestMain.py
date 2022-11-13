from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
import time
import random
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
from Signals import Signals

from signalReciever import signalReciever
from signalSender import signalSender

class signalTestMain(QMainWindow):
    #occupancySignal    = QtCore.pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.signals  = Signals()
        self.senderr  = signalSender(self.signals)
        self.reciever = signalReciever(self.signals)

App = QApplication(sys.argv)
x = signalTestMain()

sys.exit(App.exec())