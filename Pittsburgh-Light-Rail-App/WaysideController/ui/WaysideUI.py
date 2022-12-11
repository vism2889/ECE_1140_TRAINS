from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import os
from track_layout import extract_layout
import time

class TrackControllerWindow(QtWidgets.QWidget):
    def __init__(self, waysideio):
        super().__init__()

        self.redline_maintenance_mode = []
        self.greenline_maintenance_mode = []
        self.numBlocksPerController = 12

        ## Get the look up table
        # self.lookUpTable = waysideio.getLookUpTable()

        self.redline_reference = {
            'name' : 'redline',
            'controllers': [],
            'view' : [],
            'faults' : {},
            'maintenance' : []
        }

        self.greenline_reference = {
            'name' : 'greenline',
            'controllers' : [],
            'view' : [],
            'faults' : {},
            'maintenance' : []
        }

        self.waysideio_ref = waysideio
        self.FAULTS = ["OK", "BROKEN RAIL", "CIRCUIT FAILURE", "POWER FAILURE","UNDEFINED"]

    ## Main window generation
    def setupUi(self, main_window):
        self.main_window_reference = main_window

        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setStyleSheet("background-color: #747c8a;")
        self.setStyleSheet("background-color: #747c8a;")

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
        self.toolBox.setFont(QtGui.QFont())
        self.toolBox.setStyleSheet("background-color: #747c8a;")

        if os.name == 'nt':
            path = os.path.abspath(__file__.replace(__name__.replace('.', '\\')+'.py', ''))
            jsonPath = path
            trackLayoutPath = path
            path += "\\track_layout\\Track Layout & Vehicle Data vF2.xlsx - Red Line.csv"
            jsonPath += "\\track_layout\\redline-layout.json"
            trackLayoutPath += "\\track_layout\\Trains Layout - Red Line.csv"
        elif os.name == 'posix':
            path = os.path.abspath(__file__.replace(__name__.replace('.', '/')+'.py', ''))
            jsonPath = path
            trackLayoutPath = path
            path += "/track_layout/Track Layout & Vehicle Data vF2.xlsx - Red Line.csv"
            jsonPath += "/track_layout/redline-layout.json"
            trackLayoutPath += "/track_layout/Trains Layout - Red Line.csv"

        ## Extracting configuration for the red line
        redline_view_layout, redline_layout, redlineIOLayout = extract_layout.parseTrackLayout(path, jsonPath)
        redlineTrack = extract_layout.generateTrackPath(trackLayoutPath, "redline")

        self.redline_reference['total-blocks'] = redline_view_layout[0]['total-blocks']

        ######## Red Line ########
        self.redline_tab = QtWidgets.QWidget()
        self.redline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.redline_tab.setObjectName("redline_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.redline_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.redline_controllers = QtWidgets.QTabWidget(self.redline_tab)
        self.redline_controllers.setObjectName("redline_controllers")

        self.redline_tab.setStyleSheet("background-color: #747c8a;")

        for controller in redline_layout:
            ## Creating a controller tab
            self.addTab("redline", self.redline_controllers, controller, redline_layout, self.redline_reference)

        self.verticalLayout_2.addWidget(self.redline_controllers)
        self.toolBox.addItem(self.redline_tab, "")

        ######## Green Line ########
        if os.name == 'nt':
            path = os.path.abspath(__file__.replace(__name__.replace('.', '\\')+'.py', ''))
            jsonPath = path
            trackLayoutPath = path
            path += "\\track_layout\\Track Layout & Vehicle Data vF2.xlsx - Green Line.csv"
            jsonPath += "\\track_layout\\greenline-layout.json"
            trackLayoutPath += "\\track_layout\\Trains Layout - Green Line.csv"
        elif os.name == 'posix':
            path = os.path.abspath(__file__.replace(__name__.replace('.', '/')+'.py', ''))
            jsonPath = path
            trackLayoutPath = path
            path += "/track_layout/Track Layout & Vehicle Data vF2.xlsx - Green Line.csv"
            jsonPath += "/track_layout/greenline-layout.json"
            trackLayoutPath += "/track_layout/Trains Layout - Green Line.csv"

        ## Extract configuration for the greenline
        greenline_view_layout, greenline_layout, greenlineIOLayout = extract_layout.parseTrackLayout(path, jsonPath)
        greenlineTrack = extract_layout.generateTrackPath(trackLayoutPath, "greenline")

        self.greenline_reference['total-blocks'] = greenline_view_layout[0]['total-blocks']

        self.greenline_tab = QtWidgets.QWidget()
        self.greenline_tab.setGeometry(QtCore.QRect(0, 0, 782, 520))
        self.greenline_tab.setObjectName("greenline_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.greenline_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.greenline_controllers = QtWidgets.QTabWidget(self.greenline_tab)
        self.greenline_controllers.setObjectName("greenline_controllers")
        self.greenline_tab.setStyleSheet("background-color: #747c8a;")

        for controller in greenline_layout:
            ## Creating a controller tab
            self.addTab("greenline", self.greenline_controllers, controller, greenline_layout, self.greenline_reference)

        self.verticalLayout_7.addWidget(self.greenline_controllers)
        self.toolBox.addItem(self.greenline_tab, "")

        self.verticalLayout.addWidget(self.toolBox)

        self.retranslateUi(main_window)
        self.toolBox.setCurrentIndex(0)
        self.redline_controllers.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        ## Setup the WaysideIO class
        self.waysideio_ref.setUI(self)
        self.waysideio_ref.setupLine('red', redlineIOLayout, redlineTrack)
        self.waysideio_ref.setupLine('green', greenlineIOLayout, greenlineTrack)

    ## Open up a file explorer
    def dialog(self):
        loc = self.main_window_reference.sender()
        idx = int(''.join(filter(str.isdigit, loc.objectName())))
        if "redline" in loc.objectName():
            if self.redline_reference['maintenance'][idx]:
                print(f"PLC upload request to redline controller {idx}")
                file , check = QtWidgets.QFileDialog.getOpenFileName(None, "Select PLC Script",
                                                    "", "PLC Files (*.plc)")
                if os.path.exists(file):
                    with open(file) as f:
                        self.waysideio_ref.uploadPLC('red', idx, file)
                        # print(f.readline())
                        f.close()

        if "greenline" in loc.objectName():
            if self.greenline_reference['maintenance'][int(idx)]:
                print(f"PLC upload request to greenline controller {idx}")
                file , check = QtWidgets.QFileDialog.getOpenFileName(None, "Select PLC Script",
                                                    "", "PLC Files (*.plc)")
                if os.path.exists(file):
                    with open(file) as f:
                        self.waysideio_ref.uploadPLC('red', idx, file)
                        # print(f.readline())
                        f.close()

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

        # if isView:
        #     item = QtWidgets.QTableWidgetItem()
        #     item.setText("Controller")
        #     block_table.setHorizontalHeaderItem(3, item)

        block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        block_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        block_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        block_table.verticalHeader().hide()

        ## Populate tables
        for i in controller['block-occupancy']:
            row_idx = controller['block-occupancy'].index(i)
            for j in i:
                item = QtWidgets.QTableWidgetItem(str(j))
                item.setTextAlignment(4)

                if i.index(j) == 2:
                    value = ""
                    if bool(j):
                        value = 'OCCUPIED'
                    else:
                        value = 'VACANT'
                    item = QtWidgets.QTableWidgetItem(value)
                    item.setTextAlignment(4)
                    if not j:
                        item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                    else:
                        item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                block_table.setItem(row_idx, i.index(j), item)

                if isView:
                    item = QtWidgets.QTableWidgetItem(str(int(int(block_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                    item.setTextAlignment(4)
                    block_table.setItem(row_idx, 3, item)

        info['block-table'] = block_table

        verticalLayout_4.addWidget(block_table)
        gridLayout.addWidget(blockbox, 0, 0, 1, 1)

        ## Red line bottom half ##
        bottom_half = QtWidgets.QWidget(tab)
        bottom_half.setObjectName("bottom_half")
        verticalLayout_3 = QtWidgets.QVBoxLayout(bottom_half)
        verticalLayout_3.setObjectName("verticalLayout_3")

        ## Fault table ##

        fault_box = QtWidgets.QGroupBox(bottom_half)
        fault_box.setMinimumSize(QtCore.QSize(0, 150))
        fault_box.setObjectName("fault_box")
        fault_box.setTitle("Faults")

        verticalLayout_8 = QtWidgets.QVBoxLayout(fault_box)
        verticalLayout_8.setObjectName("verticalLayout_5")
        fault_table = QtWidgets.QTableWidget(fault_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fault_table.sizePolicy().hasHeightForWidth())
        fault_table.setSizePolicy(sizePolicy)
        # fault_table.setMinimumSize(QtCore.QSize(0, 450))
        fault_table.setObjectName(f"{prefix}_{layout.index(controller)}_fault_table")
        fault_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        fault_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)

        fault_table.size()
        if isView:
            fault_table.setColumnCount(4)
        else:
            fault_table.setColumnCount(3)

        fault_table.setRowCount(len(controller['block-occupancy']))

        item = QtWidgets.QTableWidgetItem()
        item.setText("Block Number")
        fault_table.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText("Section")
        fault_table.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText("Fault Message")
        fault_table.setHorizontalHeaderItem(2, item)

        # if isView:
        #     item = QtWidgets.QTableWidgetItem()
        #     item.setText("Controller")
        #     fault_table.setHorizontalHeaderItem(3, item)

        for i in controller['block-occupancy']:
            row_idx = controller['block-occupancy'].index(i)
            for j in i:
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(4)

                if i.index(j) == 2:
                    item.setText(self.FAULTS[0])
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                else:
                    item.setText(j)

                fault_table.setItem(row_idx, i.index(j), item)

                # if isView:
                #     item = QtWidgets.QTableWidgetItem(str(int(int(block_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                #     item.setTextAlignment(4)
                #     fault_table.setItem(row_idx, 3, item)

        fault_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        fault_table.verticalHeader().hide()

        info['fault-table'] = fault_table

        verticalLayout_8.addWidget(fault_table)
        gridLayout.addWidget(fault_box, 0, 1, 1, 1)

        ## Switch Status table ##
        if len(controller['switch-state']):
            switch_block = QtWidgets.QGroupBox(tab)
            switch_block.setMinimumSize(QtCore.QSize(0, 50))
            switch_block.setObjectName("switch_block")
            switch_block.setTitle("Switch States")

            verticalLayout_5 = QtWidgets.QVBoxLayout(switch_block)
            verticalLayout_5.setObjectName("verticalLayout_8")
            switch_table = QtWidgets.QTableWidget(switch_block)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)

            switch_table.setSizePolicy(sizePolicy)
            switch_table.setMinimumSize(QtCore.QSize(0, 40))
            switch_table.setObjectName("switch_table")
            switch_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
            switch_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

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

            # if isView:
            #     item = QtWidgets.QTableWidgetItem()
            #     item.setText("Controller")
            #     switch_table.setHorizontalHeaderItem(3, item)

            switch_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            switch_table.verticalHeader().hide()

            for i in controller['switch-state']:
                row_idx = controller['switch-state'].index(i)
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    item.setTextAlignment(4)
                    if i.index(j) == 2:
                        value = ""
                        if bool(j):
                            value = "ON"
                        else:
                            value = "OFF"
                        item = QtWidgets.QTableWidgetItem(value)
                        item.setTextAlignment(4)
                        if not j:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                        else:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))

                    switch_table.setItem(row_idx, i.index(j), item)

                # if isView:
                #     item = QtWidgets.QTableWidgetItem(str(int(int(switch_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                #     item.setTextAlignment(4)
                #     switch_table.setItem(row_idx, 3, item)

            info['switch-table'] = switch_table

            verticalLayout_5.addWidget(switch_table)
            verticalLayout_3.addWidget(switch_block)

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
            crossing_table.setMaximumHeight(60)
            crossing_table.setObjectName("crossing_table")
            crossing_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
            crossing_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

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

            # if isView:
            #     item = QtWidgets.QTableWidgetItem()
            #     crossing_table.setHorizontalHeaderItem(3, item)
            #     item.setText("Controller")

            crossing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            crossing_table.verticalHeader().hide()

            for i in controller['crossing-state']:
                row_idx = controller['crossing-state'].index(i)
                for j in i:
                    item = QtWidgets.QTableWidgetItem(str(j))
                    item.setTextAlignment(4)
                    if i.index(j) == 2:
                        value = ""
                        if bool(j):
                            value = "ON"
                        else:
                            value = "OFF"

                        item = QtWidgets.QTableWidgetItem(value)
                        item.setTextAlignment(4)
                        if not j:
                            item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                        else:
                            item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))

                    crossing_table.setItem(row_idx, i.index(j), item)

                    # if isView:
                    #     item = QtWidgets.QTableWidgetItem(str(int(int(crossing_table.item(row_idx, 0).text())/self.numBlocksPerController)))
                    #     item.setTextAlignment(4)
                    #     crossing_table.setItem(row_idx, 3, item)

            info['crossing-table'] = crossing_table

            verticalLayout_6.addWidget(crossing_table)
            verticalLayout_3.addWidget(crossing_box)

        gridLayout.addWidget(bottom_half, 1, 0, 1, 2)

        ## Configure Button ##
        if not isView:
            configure_button = QtWidgets.QToolButton(tab)
            configure_button.setMinimumSize(QtCore.QSize(15, 18))
            configure_button.setIconSize(QtCore.QSize(14, 14))
            configure_button.setObjectName(f"{prefix}_configure_button_{layout.index(controller)}")
            configure_button.setText("Configure Controller")
            configure_button.clicked.connect(lambda: self.dialog()) ## Set Button Click Signal
            gridLayout.addWidget(configure_button, 2, 0, 1, 1)

        if isView:
            controllers.addTab(tab, f"View")
        else:
            controllers.addTab(tab, f"Controller {layout.index(controller) + 1}")

        if isView:
            reference['view'].append(info)
        else:
            reference['controllers'].append(info)
            reference['maintenance'].append(False)

        gridLayout.addWidget(blockbox, 0, 0, 1, 1)


    def setBlockState(self, line, block_num, state):
        if block_num <= 0:
            print("Err: invalid block number")

        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']

        value = ""
        if state:
            value = "OCCUPIED"
        else:
            value = "VACANT"

        if line == 'red':
            ## Calculate index
            for i in controller_indices:

                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if state:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                else:
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))

                self.redline_reference['controllers'][i[0]]['block-table'].setItem(i[1], 2, item)

        if line == 'green':
            for i in controller_indices:

                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if state:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                else:
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                self.greenline_reference['controllers'][i[0]]['block-table'].setItem(i[1], 2, item)

    def setFaultState(self, line, block_num, fault_ids=[]):
        if block_num <= 0:
                print("Err: invalid block number")

        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']
        text_str=""

        for i,fault in enumerate(fault_ids):
            text_str+=self.FAULTS[fault]
            if i != len(fault_ids)-1:
                text_str+= "\n"

        if line == 'red':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem()
                item.setText(text_str)
                item.setTextAlignment(4)

                if len(fault_ids) > 0:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                elif len(fault_ids) == 0:
                    item.setText("OK")
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))

                self.redline_reference['controllers'][i[0]]['fault-table'].setItem(i[1], 2, item)

        if line == 'green':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem()
                item.setText(text_str)
                item.setTextAlignment(4)

                if len(fault_ids) > 0:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                elif len(fault_ids) == 0:
                    item.setText("OK")
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                self.greenline_reference['controllers'][i[0]]['fault-table'].setItem(i[1], 2, item)

        self.checkFaults(line, block_num)

    def checkFaults(self, line, block_num):
        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']
        good = True

        if line == 'red':
            for i in controller_indices:
                fault_table = self.redline_reference['controllers'][i[0]]['fault-table']
                size = self.waysideio_ref.getNumBlocks(line, i[0])
                for j in range(size):
                    # if fault_table.item(j[1],2).text() != 'OK':
                    if fault_table.item(j,2).text() != 'OK':
                        self.redline_controllers.setTabIcon(i[0], QtGui.QIcon("warning.png"))
                        good = False
            if good:
                self.redline_controllers.setTabIcon(i[0], QtGui.QIcon())

        if line == 'green':
            for i in controller_indices:
                fault_table = self.greenline_reference['controllers'][i[0]]['fault-table']
                size = self.waysideio_ref.getNumBlocks(line, i[0])
                for j in range(size):
                    if fault_table.item(j,2).text() != 'OK':
                        self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon("warning.png"))
                        good = False
            if good:
                self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon())
        if good:
            self.checkMaintenance(line, block_num)

        return good

    def setSwitchState(self, line, block_num, state):
        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']

        value = ""
        if state:
            value = "ON"
        else:
            value = "OFF"

        if line == 'red':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if state:
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                else:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                controller_table = self.redline_reference['controllers'][i[0]]
                if 'switch-table' in controller_table:
                    for row in range(controller_table['switch-table'].rowCount()):
                        if controller_table['switch-table'].item(row, 0).text() == str(block_num):
                            controller_table['switch-table'].setItem(row, 2, item)
                            break

        if line == 'green':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if state:
                    item.setBackground(QtGui.QColor(0xbf, 0xe3, 0xb4))
                else:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))
                controller_table = self.greenline_reference['controllers'][i[0]]

                if 'switch-table' in controller_table:
                    for row in range(controller_table['switch-table'].rowCount()):
                        if controller_table['switch-table'].item(row, 0).text() == str(block_num):
                            controller_table['switch-table'].setItem(row, 2, item)
                            break

    def setCrossingState(self, line, block_num, state):
        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']

        value = ""

        if state:
            value = "ON"
        else:
            value = "OFF"

        if line == 'red':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if value:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                controller_table = self.redline_reference['controllers'][i[0]]
                if 'crossing-table' in controller_table:
                    for row in range(controller_table['crossing-table'].rowCount()):
                        if controller_table['crossing-table'].item(row, 0).text() == str(block_num):
                            controller_table['crossing-table'].setItem(row, 2, item)
                            break

        if line == 'green':
            for i in controller_indices:
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(4)

                if value:
                    item.setBackground(QtGui.QColor(0xf4, 0x71, 0x74))

                controller_table = self.greenline_reference['controllers'][i[0]]
                if 'crossing-table' in controller_table:
                    for row in range(controller_table['crossing-table'].rowCount()):
                        if controller_table['crossing-table'].item(row, 0).text() == str(block_num):
                            controller_table['crossing-table'].setItem(row, 2, item)
                            break

    def setMaintenance(self, line, block_num, value):

        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']
        good = self.checkFaults(line, block_num)

        if line == 'red':
            for i in controller_indices:
                self.redline_reference['maintenance'][i[0]] = value
                if value:
                    if good: self.redline_controllers.setTabIcon(i[0], QtGui.QIcon("alert.png"))
                    self.redline_reference['controllers'][i[0]]['block-table'].item(i[1], 0).setIcon(QtGui.QIcon("alert.png"))
                else:
                    if good: self.redline_controllers.setTabIcon(i[0], QtGui.QIcon())
                    self.redline_reference['controllers'][i[0]]['block-table'].item(i[1], 0).setIcon(QtGui.QIcon())

        if line == 'green':
            for i in controller_indices:
                self.greenline_reference['maintenance'][i[0]] = value
                if value:
                    if good: self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon("alert.png"))
                    self.greenline_reference['controllers'][i[0]]['block-table'].item(i[1], 0).setIcon(QtGui.QIcon("alert.png"))
                else:
                    if good: self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon())
                    self.greenline_reference['controllers'][i[0]]['block-table'].item(i[1], 0).setIcon(QtGui.QIcon())

    def checkMaintenance(self, line, block_num):
        controller_indices = self.waysideio_ref.lookupBlock(line, block_num)['controller']
        if line == 'red':
            for i in controller_indices:
                value = self.redline_reference['maintenance'][i[0]]
                if value:
                    self.redline_controllers.setTabIcon(i[0], QtGui.QIcon("alert.png"))
                else:
                    self.redline_controllers.setTabIcon(i[0], QtGui.QIcon())

        if line == 'green':
            for i in controller_indices:
                value = self.greenline_reference['maintenance'][i[0]]
                if value:
                    self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon("alert.png"))
                else:
                    self.greenline_controllers.setTabIcon(i[0], QtGui.QIcon())

    def getNumRedLineBlocks(self):
        return self.redline_reference['total-blocks']

    def getNumGreenLineBlocks(self):
        return self.greenline_reference['total-blocks']

    ## LOOKING TO GET RID OF THIS STUPID FUNCTION
    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Track Controller"))

        self.toolBox.setItemText(self.toolBox.indexOf(self.redline_tab), _translate("main_window", "Red Line"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.greenline_tab), _translate("main_window", "Green Line"))