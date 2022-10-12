# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from ast import mod
from copy import deepcopy
from signal import sigwait
from tkinter import dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from track_layout import extract_layout

class TrainControllerWindow(object):
    def __init__(self):
        self.maintenance_mode = True
        self.numBlocksPerController = 12

        self.redline_reference = {
            'controllers': [],
            'view' : []
        }

        self.greenline_reference = {
            'controllers' : [],
            'view' : []
        }

    def setupUi(self, main_window):
        self.main_window_reference = main_window

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

        redline_view_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Red Line.csv", 0)
        redline_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Red Line.csv", self.numBlocksPerController)

        ######## Red Line ########
        self.redline_tab = QtWidgets.QWidget()
        self.redline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.redline_tab.setObjectName("redline_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.redline_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.redline_controllers = QtWidgets.QTabWidget(self.redline_tab)
        self.redline_controllers.setObjectName("redline_controllers")

        for controller in redline_view_layout:
            ## Creating a view tab
            self.addTab("redline_view", self.redline_controllers, controller, redline_view_layout, self.redline_reference['view'], True)

        for controller in redline_layout:
            ## Creating a tab
            self.addTab("redline", self.redline_controllers, controller, redline_layout, self.redline_reference['controllers'])

        self.verticalLayout_2.addWidget(self.redline_controllers)
        self.toolBox.addItem(self.redline_tab, "")

        ######## Green Line ########
        greenline_view_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv", 0)
        greenline_layout = extract_layout.parseTrackLayout("track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv", self.numBlocksPerController)

        self.greenline_tab = QtWidgets.QWidget()
        self.greenline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.greenline_tab.setObjectName("greenline_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.greenline_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.greenline_controllers = QtWidgets.QTabWidget(self.greenline_tab)
        self.greenline_controllers.setObjectName("greenline_controllers")

        for controller in greenline_view_layout:
            ## Creating a view tab
            self.addTab("greenline_view", self.greenline_controllers, controller, greenline_view_layout, self.greenline_reference['view'], True)

        for controller in greenline_layout:
            ## Creating a controller tab
            self.addTab("greenline", self.greenline_controllers, controller, greenline_layout, self.greenline_reference['controllers'])

        self.verticalLayout_7.addWidget(self.greenline_controllers)
        self.toolBox.addItem(self.greenline_tab, "")

        self.verticalLayout.addWidget(self.toolBox)

        self.retranslateUi(main_window)
        self.toolBox.setCurrentIndex(0)
        self.redline_controllers.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def dialog(self):
        loc = self.main_window_reference.sender()
        print(f"PLC upload request to {loc.objectName()}")

        if self.maintenance_mode:
           file , check = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")

    def addTab(self, prefix, controllers, controller, layout, reference, isView=False):
        ## Dictionary information for reference
        info = {}

        tab = QtWidgets.QWidget()
        tab.setObjectName(f"{prefix}_controller_tab_{layout.index(controller)}")
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
        if isView:
            block_table.setColumnCount(4)
        else:
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

        if isView:
            item = QtWidgets.QTableWidgetItem()
            item.setText("Controller")
            block_table.setHorizontalHeaderItem(3, item)

        block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        block_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        block_table.verticalHeader().hide()

        for i in controller['block-occupancy']:
            row_idx = controller['block-occupancy'].index(i)
            for j in i:
                item = QtWidgets.QTableWidgetItem(str(j))
                if i.index(j) == 2:
                    if not j:
                        item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                    else:
                        item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                block_table.setItem(row_idx, i.index(j), item)

                if isView:
                    item = QtWidgets.QTableWidgetItem(str(int(int(block_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                    block_table.setItem(row_idx, 3, item)

        info['block-table'] = block_table

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

            if isView:
                switch_table.setColumnCount(4)
            else:
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

            if isView:
                item = QtWidgets.QTableWidgetItem()
                item.setText("Controller")
                switch_table.setHorizontalHeaderItem(3, item)

            switch_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            switch_table.verticalHeader().hide()

            for i in controller['switch-state']:
                row_idx = controller['switch-state'].index(i)
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    if i.index(j) == 2:
                        if not j:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                        else:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                    switch_table.setItem(row_idx, i.index(j), item)

                if isView:
                    item = QtWidgets.QTableWidgetItem(str(int(int(switch_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                    switch_table.setItem(row_idx, 3, item)

            info['switch-table'] = switch_table

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
        fault_table.setObjectName(f"{prefix}_{layout.index(controller)}_fault_table")

        if isView:
            fault_table.setColumnCount(4)
        else:
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

        if isView:
            item = QtWidgets.QTableWidgetItem()
            item.setText("Controller")
            fault_table.setHorizontalHeaderItem(3, item)

        fault_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        info['fault-table'] = fault_table

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

            if isView:
                crossing_table.setColumnCount(4)
            else:
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

            if isView:
                item = QtWidgets.QTableWidgetItem()
                crossing_table.setHorizontalHeaderItem(3, item)
                item.setText("Controller")

            crossing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            crossing_table.verticalHeader().hide()

            for i in controller['crossing-state']:
                row_idx = controller['crossing-state'].index(i)
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    if i.index(j) == 2:
                        if not j:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                        else:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                    crossing_table.setItem(row_idx, i.index(j), item)

                    if isView:
                        item = QtWidgets.QTableWidgetItem(str(int(int(crossing_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                        crossing_table.setItem(row_idx, 3, item)

            info['crossing-table'] = crossing_table

            verticalLayout_6.addWidget(crossing_table)
            verticalLayout_3.addWidget(crossing_box)

        gridLayout.addWidget(bottom_half, 1, 0, 1, 2)

        ## Configure Button ##
        if not isView:
            configure_button = QtWidgets.QToolButton(tab)
            configure_button.setMinimumSize(QtCore.QSize(10, 18))
            configure_button.setIconSize(QtCore.QSize(14, 14))
            configure_button.setObjectName(f"{prefix}_{layout.index(controller)}_configure_button")
            configure_button.setText("Configure Controller")
            configure_button.clicked.connect(lambda: self.dialog()) ## Set Button Click Signal
            gridLayout.addWidget(configure_button, 2, 0, 1, 1)

        if isView:
            controllers.addTab(tab, f"View")
        else:
            controllers.addTab(tab, f"Controller {layout.index(controller)}")

        reference.append(info)

        gridLayout.addWidget(blockbox, 0, 0, 1, 1)


    def setBlockState(self, line, block_num, value):
        if block_num <= 0:
            print("Err: invalid block number")

        controller_idx = int((block_num-1)/self.numBlocksPerController)
        row_idx = (block_num-1) % self.numBlocksPerController
        # print(f"block number {block_num} is at controller index {controller_idx}, row {row_idx}")

        item = QtWidgets.QTableWidgetItem(str(value))
        item2 = QtWidgets.QTableWidgetItem(str(value))
        if value:
            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
            item2.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
        else:
            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
            item2.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

        if line == 'red':
            ## Calculate index
            self.redline_reference['controllers'][controller_idx]['block-table'].setItem(row_idx, 2, item)
            self.redline_reference['view'][0]['block-table'].setItem(block_num-1, 2, item2)

        if line == 'green':
            self.greenline_reference['controllers'][controller_idx]['block-table'].setItem(row_idx, 2, item)
            self.greenline_reference['view'][0]['block-table'].setItem(block_num-1, 2, item2)


    def setFaultState(self, line, block_num, value):
        if block_num <= 0:
                print("Err: invalid block number")

        controller_idx = int((block_num-1)/self.numBlocksPerController)
        row_idx = (block_num-1) % self.numBlocksPerController
        # print(f"block number {block_num} is at controller index {controller_idx}, row {row_idx}")

        item = QtWidgets.QTableWidgetItem(str(value))
        item2 = QtWidgets.QTableWidgetItem(str(value))
        if value:
            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
            item2.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
        else:
            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
            item2.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

        if line == 'red':
            self.redline_reference['controllers'][controller_idx]['fault-table'].setItem(row_idx, 2, item)
            self.redline_reference['view'][0]['fault-table'].setItem(block_num-1, 2, item2)

        if line == 'green':
            self.greenline_reference['controllers'][controller_idx]['fault-table'].setItem(row_idx, 2, item)
            self.greenline_reference['view'][0]['fault-table'].setItem(block_num-1, 2, item2)


    def setSwitchState(self, line, block_num, value):
        controller_idx = int((block_num-1)/self.numBlocksPerController)

        item = QtWidgets.QTableWidgetItem(str(value))
        item2 = QtWidgets.QTableWidgetItem(str(value))

        if line == 'red':
            for i in self.redline_reference['controllers'][controller_idx]
            self.redline_reference['controllers'][controller_idx]['fault-table'].setItem(row_idx, 2, item)
            self.redline_reference['view'][0]['fault-table'].setItem(block_num-1, 2, item2)

        if line == 'green':
            self.greenline_reference['controllers'][controller_idx]['fault-table'].setItem(row_idx, 2, item)
            self.greenline_reference['view'][0]['fault-table'].setItem(block_num-1, 2, item2)



    def setCrossingState(self, line, block_num):

        return

    def loadTestWindow():
        ## launch Test Window GUI
        # TestWindow(self)
        return

    ## LOOKING TO GET RID OF THIS STUPID FUNCTION
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Track Controller"))

        self.toolBox.setItemText(self.toolBox.indexOf(self.redline_tab), _translate("main_window", "Red Line"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.greenline_tab), _translate("main_window", "Green Line"))
