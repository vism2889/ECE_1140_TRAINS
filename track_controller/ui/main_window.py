# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from copy import deepcopy
from tkinter import dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from track_layout import extract_layout

def makeBlockWidget(prefix, parent):
        blockbox = QtWidgets.QGroupBox(parent)
        blockbox.setObjectName(prefix + "_blockbox")
        verticalLayout_4 = QtWidgets.QVBoxLayout(blockbox)
        verticalLayout_4.setObjectName(prefix + "_verticalLayout")
        block_table = QtWidgets.QTableWidget(blockbox)
        block_table.setObjectName(prefix + "_block_table")
        block_table.setColumnCount(3)
        block_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        block_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        block_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        block_table.setHorizontalHeaderItem(2, item)
        block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        block_table.verticalHeader().hide()
        verticalLayout_4.addWidget(block_table)
        return verticalLayout_4


class Ui_main_window(object):
    def __init__(self):
        self.maintenance_mode = False

    def dialog(self, line, id):
        print(f"PLC upload to {line}line, controller {id}")
        if self.maintenance_mode:
           file , check = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")

    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(main_window)
        self.verticalLayout.setObjectName("verticalLayout")

        ## "Toolbox" ##
        self.toolBox = QtWidgets.QToolBox(main_window)
        self.toolBox.setObjectName("toolBox")

        redline_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Red Line.csv", 15)

        ######## Red Line ########
        self.redline_tab = QtWidgets.QWidget()
        self.redline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.redline_tab.setObjectName("redline_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.redline_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.redline_controllers = QtWidgets.QTabWidget(self.redline_tab)
        self.redline_controllers.setObjectName("redline_controllers")

        for controller in redline_layout:
            controller_idx = redline_layout.index(controller)
            ## Creating a controller tab
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"controller_tab_{redline_layout.index(controller)}")
            gridLayout = QtWidgets.QGridLayout(tab)
            gridLayout.setObjectName("gridLayout")

            ## redline block occupancy table ##
            blockbox = QtWidgets.QGroupBox(tab)
            blockbox.setObjectName("blockbox")
            blockbox.setTitle("Block Occupancy")

            verticalLayout_4 = QtWidgets.QVBoxLayout(blockbox)
            verticalLayout_4.setObjectName("verticalLayout_4")
            block_table = QtWidgets.QTableWidget(blockbox)
            block_table.setObjectName("block_table")
            block_table.setColumnCount(3)
            block_table.setRowCount(len(controller['block-occupancy']))

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block Number")
            block_table.setHorizontalHeaderItem(0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Section")
            block_table.setHorizontalHeaderItem(1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block State")
            block_table.setHorizontalHeaderItem(2, item)

            block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            block_table.verticalHeader().hide()
            block_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            ## Set the items in the table ##
            for i in controller['block-occupancy']:
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    if i.index(j) == 2:
                        if not j:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                        else:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                    block_table.setItem(controller['block-occupancy'].index(i), i.index(j), item)

            verticalLayout_4.addWidget(block_table)
            gridLayout.addWidget(blockbox, 0, 0, 1, 1)

            if len(controller['switch-state']):
                ## Switch Status table ##
                switch_block = QtWidgets.QGroupBox(tab)
                switch_block.setMinimumSize(QtCore.QSize(0, 180))
                switch_block.setObjectName("switch_block")
                switch_block.setTitle("Switch States")

                verticalLayout_8 = QtWidgets.QVBoxLayout(switch_block)
                verticalLayout_8.setObjectName("verticalLayout_8")
                switch_table = QtWidgets.QTableWidget(switch_block)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(switch_table.sizePolicy().hasHeightForWidth())
                switch_table.setSizePolicy(sizePolicy)
                switch_table.setMinimumSize(QtCore.QSize(0, 40))
                switch_table.setObjectName("switch_table")
                switch_table.setColumnCount(3)
                switch_table.setRowCount(len(controller['switch-state']))

                item = QtWidgets.QTableWidgetItem()
                item.setText("Block Number")
                switch_table.setHorizontalHeaderItem(0, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText("Section")
                switch_table.setHorizontalHeaderItem(1, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText("Switch State")
                switch_table.setHorizontalHeaderItem(2, item)

                switch_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                switch_table.verticalHeader().hide()
                switch_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

                ## Set the items in the table ##
                for i in controller['switch-state']:
                    for j in i:
                        item = QtWidgets.QTableWidgetItem(str(j))
                        if i.index(j) == 2:
                            if not j:
                                item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                            else:
                                item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                        switch_table.setItem(controller['switch-state'].index(i), i.index(j), item)

                verticalLayout_8.addWidget(switch_table)
                gridLayout.addWidget(switch_block, 0, 1, 1, 1)

            ## Red line bottom half ##
            bottom_half = QtWidgets.QWidget(tab)
            bottom_half.setObjectName("bottom_half")
            verticalLayout_3 = QtWidgets.QVBoxLayout(bottom_half)
            verticalLayout_3.setObjectName("verticalLayout_3")

            ## Fault table ##
            fault_box = QtWidgets.QGroupBox(bottom_half)
            fault_box.setMinimumSize(QtCore.QSize(0, 140))
            fault_box.setObjectName("fault_box")
            fault_box.setTitle("Faults")

            verticalLayout_5 = QtWidgets.QVBoxLayout(fault_box)
            verticalLayout_5.setObjectName("verticalLayout_5")
            fault_table = QtWidgets.QTableWidget(fault_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(fault_table.sizePolicy().hasHeightForWidth())
            fault_table.setSizePolicy(sizePolicy)
            fault_table.setMinimumSize(QtCore.QSize(0, 60))
            fault_table.setObjectName(f"redline_controller_{redline_layout.index(controller)}_fault_table")
            fault_table.setColumnCount(3)
            fault_table.setRowCount(0)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block Number")
            fault_table.setHorizontalHeaderItem(0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Section")
            fault_table.setHorizontalHeaderItem(1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Fault Message")
            fault_table.setHorizontalHeaderItem(2, item)

            fault_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            verticalLayout_5.addWidget(fault_table)
            verticalLayout_3.addWidget(fault_box)

            ## Crossing status table ##
            if len(controller['crossing-state']):
                crossing_box = QtWidgets.QGroupBox(bottom_half)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(crossing_box.sizePolicy().hasHeightForWidth())
                crossing_box.setSizePolicy(sizePolicy)
                crossing_box.setMinimumSize(QtCore.QSize(0, 10))
                crossing_box.setObjectName("crossing_box")
                crossing_box.setTitle("Crossing State")
                verticalLayout_6 = QtWidgets.QVBoxLayout(crossing_box)
                verticalLayout_6.setObjectName("verticalLayout_6")
                crossing_table = QtWidgets.QTableWidget(crossing_box)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(crossing_table.sizePolicy().hasHeightForWidth())
                crossing_table.setSizePolicy(sizePolicy)
                crossing_table.setMinimumSize(QtCore.QSize(0, 40))
                crossing_table.setObjectName("crossing_table")
                crossing_table.setColumnCount(3)
                crossing_table.setRowCount(len(controller['crossing-state']))

                item = QtWidgets.QTableWidgetItem()
                item.setText("Block Number")
                crossing_table.setHorizontalHeaderItem(0, item)

                item = QtWidgets.QTableWidgetItem()
                crossing_table.setHorizontalHeaderItem(1, item)
                item.setText("Section")

                item = QtWidgets.QTableWidgetItem()
                crossing_table.setHorizontalHeaderItem(2, item)
                item.setText("Crossing State")

                crossing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                crossing_table.verticalHeader().hide()

                for i in controller['crossing-state']:
                    for j in i:
                        item = QtWidgets.QTableWidgetItem(str(j))
                        if i.index(j) == 2:
                            if not j:
                                item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                            else:
                                item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                        crossing_table.setItem(controller['crossing-state'].index(i), i.index(j), item)

                verticalLayout_6.addWidget(crossing_table)
                verticalLayout_3.addWidget(crossing_box)

            gridLayout.addWidget(bottom_half, 1, 0, 1, 2)

            ## Configure Button ##
            configure_button = QtWidgets.QToolButton(tab)
            configure_button.setMinimumSize(QtCore.QSize(10, 18))
            configure_button.setIconSize(QtCore.QSize(14, 14))
            configure_button.setObjectName(f"redline_controller_{redline_layout.index(controller)}_configure_button")
            configure_button.setText("Configure Controller")
            configure_button.clicked.connect(lambda: self.dialog("red", deepcopy(controller_idx))) ## Set Button Click Signal

            gridLayout.addWidget(configure_button, 2, 0, 1, 1)
            self.redline_controllers.addTab(tab, f"Controller {redline_layout.index(controller)}")

        self.verticalLayout_2.addWidget(self.redline_controllers)
        self.toolBox.addItem(self.redline_tab, "")

        ######## Green Line ########
        greenline_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv", 15)

        self.greenline_tab = QtWidgets.QWidget()
        self.greenline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.greenline_tab.setObjectName("greenline_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.greenline_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.greenline_controllers = QtWidgets.QTabWidget(self.greenline_tab)
        self.greenline_controllers.setObjectName("greenline_controllers")

        for controller in greenline_layout:
            ## Creating a controller tab
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"controller_tab_{greenline_layout.index(controller)}")
            gridLayout = QtWidgets.QGridLayout(tab)
            gridLayout.setObjectName("gridLayout")

            ## redline block occupancy table ##
            blockbox = QtWidgets.QGroupBox(tab)
            blockbox.setObjectName("blockbox")
            blockbox.setTitle("Block Occupancy")

            verticalLayout_4 = QtWidgets.QVBoxLayout(blockbox)
            verticalLayout_4.setObjectName("verticalLayout_4")
            block_table = QtWidgets.QTableWidget(blockbox)
            block_table.setObjectName("block_table")
            block_table.setColumnCount(3)
            block_table.setRowCount(len(controller['block-occupancy']))

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block Number")
            block_table.setHorizontalHeaderItem(0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Section")
            block_table.setHorizontalHeaderItem(1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block State")
            block_table.setHorizontalHeaderItem(2, item)

            block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            block_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            block_table.verticalHeader().hide()

            for i in controller['block-occupancy']:
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    if i.index(j) == 2:
                        if not j:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                        else:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                    block_table.setItem(controller['block-occupancy'].index(i), i.index(j), item)

            verticalLayout_4.addWidget(block_table)
            gridLayout.addWidget(blockbox, 0, 0, 1, 1)

            ## Switch Status table ##
            if len(controller['switch-state']):
                switch_block = QtWidgets.QGroupBox(tab)
                switch_block.setMinimumSize(QtCore.QSize(0, 180))
                switch_block.setObjectName("switch_block")
                switch_block.setTitle("Switch States")

                verticalLayout_8 = QtWidgets.QVBoxLayout(switch_block)
                verticalLayout_8.setObjectName("verticalLayout_8")
                switch_table = QtWidgets.QTableWidget(switch_block)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(switch_table.sizePolicy().hasHeightForWidth())
                switch_table.setSizePolicy(sizePolicy)
                switch_table.setMinimumSize(QtCore.QSize(0, 40))
                switch_table.setObjectName("switch_table")
                switch_table.setColumnCount(3)
                switch_table.setRowCount(len(controller['switch-state']))

                item = QtWidgets.QTableWidgetItem()
                item.setText("Block Number")
                switch_table.setHorizontalHeaderItem(0, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText("Section")
                switch_table.setHorizontalHeaderItem(1, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText("Switch State")
                switch_table.setHorizontalHeaderItem(2, item)

                switch_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                switch_table.verticalHeader().hide()

                for i in controller['switch-state']:
                    for j in i:
                        item = QtWidgets.QTableWidgetItem(str(j))
                        if i.index(j) == 2:
                            if not j:
                                item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                            else:
                                item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                        switch_table.setItem(controller['switch-state'].index(i), i.index(j), item)

                verticalLayout_8.addWidget(switch_table)
                gridLayout.addWidget(switch_block, 0, 1, 1, 1)

            ## Red line bottom half ##
            bottom_half = QtWidgets.QWidget(tab)
            bottom_half.setObjectName("bottom_half")
            verticalLayout_3 = QtWidgets.QVBoxLayout(bottom_half)
            verticalLayout_3.setObjectName("verticalLayout_3")

            ## Fault table ##
            fault_box = QtWidgets.QGroupBox(bottom_half)
            fault_box.setMinimumSize(QtCore.QSize(0, 140))
            fault_box.setObjectName("fault_box")
            fault_box.setTitle("Faults")

            verticalLayout_5 = QtWidgets.QVBoxLayout(fault_box)
            verticalLayout_5.setObjectName("verticalLayout_5")
            fault_table = QtWidgets.QTableWidget(fault_box)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(fault_table.sizePolicy().hasHeightForWidth())
            fault_table.setSizePolicy(sizePolicy)
            fault_table.setMinimumSize(QtCore.QSize(0, 60))
            fault_table.setObjectName(f"greenline_controller_{greenline_layout.index(controller)}_fault_table")
            fault_table.setColumnCount(3)
            fault_table.setRowCount(0)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Block Number")
            fault_table.setHorizontalHeaderItem(0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Section")
            fault_table.setHorizontalHeaderItem(1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText("Fault Message")
            fault_table.setHorizontalHeaderItem(2, item)
            fault_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


            verticalLayout_5.addWidget(fault_table)
            verticalLayout_3.addWidget(fault_box)

            ## Crossing status table ##
            if len(controller['crossing-state']):
                crossing_box = QtWidgets.QGroupBox(bottom_half)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(crossing_box.sizePolicy().hasHeightForWidth())
                crossing_box.setSizePolicy(sizePolicy)
                crossing_box.setMinimumSize(QtCore.QSize(0, 20))
                crossing_box.setObjectName("crossing_box")
                crossing_box.setTitle("Crossing State")
                verticalLayout_6 = QtWidgets.QVBoxLayout(crossing_box)
                verticalLayout_6.setObjectName("verticalLayout_6")
                crossing_table = QtWidgets.QTableWidget(crossing_box)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(crossing_table.sizePolicy().hasHeightForWidth())
                crossing_table.setSizePolicy(sizePolicy)
                crossing_table.setMinimumSize(QtCore.QSize(0, 40))
                crossing_table.setObjectName("crossing_table")
                crossing_table.setColumnCount(3)
                crossing_table.setRowCount(len(controller['crossing-state']))

                item = QtWidgets.QTableWidgetItem()
                item.setText("Block Number")
                crossing_table.setHorizontalHeaderItem(0, item)

                item = QtWidgets.QTableWidgetItem()
                crossing_table.setHorizontalHeaderItem(1, item)
                item.setText("Section")

                item = QtWidgets.QTableWidgetItem()
                crossing_table.setHorizontalHeaderItem(2, item)
                item.setText("Crossing State")

                crossing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                crossing_table.verticalHeader().hide()

                for i in controller['crossing-state']:
                    for j in i:
                        item = QtWidgets.QTableWidgetItem(str(j))
                        if i.index(j) == 2:
                            if not j:
                                item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                            else:
                                item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                        crossing_table.setItem(controller['crossing-state'].index(i), i.index(j), item)

                verticalLayout_6.addWidget(crossing_table)
                verticalLayout_3.addWidget(crossing_box)

            gridLayout.addWidget(bottom_half, 1, 0, 1, 2)

            ## Configure Button ##
            configure_button = QtWidgets.QToolButton(tab)
            configure_button.setMinimumSize(QtCore.QSize(10, 18))
            configure_button.setIconSize(QtCore.QSize(14, 14))
            configure_button.setObjectName(f"greenline_controller_{greenline_layout.index(controller)}_configure_button")
            configure_button.setText("Configure Controller")
            configure_button.clicked.connect(lambda: self.dialog("green", greenline_layout.index(controller))) ## Set Button Click Signal

            gridLayout.addWidget(configure_button, 2, 0, 1, 1)
            self.greenline_controllers.addTab(tab, f"Controller {greenline_layout.index(controller)}")

        self.verticalLayout_7.addWidget(self.greenline_controllers)
        self.toolBox.addItem(self.greenline_tab, "")

        self.verticalLayout.addWidget(self.toolBox)

        self.retranslateUi(main_window)
        self.toolBox.setCurrentIndex(0)
        self.redline_controllers.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    ## LOOKING TO GET RID OF THIS STUPID FUNCTION
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Track Controller"))

        self.toolBox.setItemText(self.toolBox.indexOf(self.redline_tab), _translate("main_window", "Red Line"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.greenline_tab), _translate("main_window", "Green Line"))
