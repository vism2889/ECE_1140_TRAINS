#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/09/2022
# FILENAME: TrackModelTestInterfaceUI.py
# DESCRIPTION:
#
##############################################################################

import sys
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

class TestUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model - Test Interface')
        self.left = 650
        self.top = 10
        self.width = 640
        self.height = 540
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.label = QLabel("Pittsburgh Light Rail - Track Model Testing Interface", self)
        self.label.move(10,10)