







import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
#from LayoutParser import LayoutParser
#from TrackModelTestInterfaceUI import TestUI
#from infraParser import InfraParser

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title         = 'Train Model - Pittsburgh Light Rail'
        self.left          = 10
        self.top           = 10
        self.width         = 640
        self.height        = 540
        self.lineNames     = []
        self.lines         = []
        self.stations      = []
        self.crossings     = []
        self.switches      = []
        self.infraCounts   = [] # holds the count  for  stations, switches, crossings
        self.currLineIndex = None
        self.layoutFile    = None
        self.testUI        = TestUI()
        self.testList      = []
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


