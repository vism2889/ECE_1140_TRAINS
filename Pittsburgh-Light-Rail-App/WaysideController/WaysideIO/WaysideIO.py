import os
import importlib
# import threading
from PLCParser import PLCParser
from PyQt5.QtWidgets import QWidget


## testing
from track_layout import extract_layout

class Controller():
    def __init__(self, line, controllerNum, layout, ui, parent):

        self.line = line
        self.layout = layout
        self.ui = ui
        self.parent = parent
        self.logger = parent.logger

        ## Function to run PLC program
        self.plc = None
        self.plcGood = True

        ##
        self.maintenance = True

        ## Setup layout
        self.track = {
            'block' : {}, ## block occupancy
            'switch' : {}, ##
            'crossing': {},
            'block-states' : {}, ## block failures as one-hot encoded
            'block-maintenance': {},
            'sections' : {}
        }

        for section in self.layout['sections']:
            ## Blocks
            for block in self.layout['sections'][section]['blocks']:
                self.track['block'][block[0]] = block[2]
                self.track['block-states'][block[0]] = 0x00

            ## Switches
            for switch in self.layout['sections'][section]['switches']:
                self.track['switch'][switch] = False

            ## Crossings
            for crossing in self.layout['sections'][section]['crossing']:
                self.track['crossing'][crossing] = False

        self.id = controllerNum

        ## Setup PLC interface
        self.parser = PLCParser(controllerNum)
        if self.line == 'green':
            file = open(f"plc/controller{self.id}.plc")
            self.uploadPLC(file)
            self.maintenance = False

    ## Get Current Track State
    def getTrack(self):
        return self.track

    ## Update block occupancies
    def updateOccupancy(self, blockNum, state):
        ## Update block
        self.track['block'][str(blockNum)] = state
        self.ui.setBlockState(self.line, blockNum, state)

        ## Run PLC program
        self.run()

        ## update outputs
        self.updateSwitch()
        self.updateCrossing()

        return self.track['block']

    ## Update block failures
    def updateFailures(self, blockNum, failures):
        self.track['block-states'][blockNum] = failures

        ## Extract the individual faults
        faults = []

        ## Track Failure (0x01)
        if 0x01 & failures:
            self.logger.debug(f'track failure on block {blockNum}')
            faults.append(0x01)
        ## Circuit Failure
        if 0x02 & failures:
            self.logger.debug(f'circuit failure on block {blockNum}')
            faults.append(0x02)
        ## Power Failure
        if 0x04 & failures:
            self.logger.debug(f'power failure on block {blockNum}')
            faults.append(0x03)

        self.ui.setFaultState(self.line, blockNum, faults)
        ## Run PLC program
        # self.run()
        return self.track['block-states']

    def updateMaintenance(self, blockNum, state):
        self.track['block-maintenance'][blockNum] = state
        self.ui.setMaintenance(self.line, blockNum, state)

        ## Run PLC program
        self.run()

        return self.track['block-maintenance']

    ## Switches and crossing only get update with the PLC program
    def updateSwitch(self):
        for switch in self.track['switch']:
            self.parent.setSwitch(self.line, switch, self.track['switch'][switch])
            self.ui.setSwitchState(self.line, int(switch), self.track['switch'][switch])

        return self.track['switch']

    def updateCrossing(self):
        for crossing in self.track['crossing']:
            self.parent.setCrossing(self.line, crossing, self.track['crossing'][crossing])
            self.ui.setCrossingState(self.line, int(crossing), self.track['crossing'][crossing])

        ## Run PLC program
        return self.track['crossing']

    ## Toggle maintenance mode (FOR THE CONTROLLER)
    def toggleMaintence(self):
        self.maintenance != self.maintenance
        return self.maintenance

    ## Run the PLCs
    def run(self):
        if self.plcGood:
            try:
                self.plc(self.track)
            except:
                print(f'Error: PLC script cannot run (controller{self.id})')
                self.plcGood = False

    ## Upload a PLC ##
    def uploadPLC(self, file):
        if self.maintenance:
            modname = self.parser.parseFile(file)
            try:
                mod = importlib.import_module("plc."+modname)
                mod.run(self.track)
            except ImportError:
                print(f"Errror: Could not import plc script for controller {self.id}")
                self.plcGood = False
            else:
                self.parent.logger.debug(f'Plc has been loaded for controller {self.id}')
                # print(f'Plc has been loaded for controller {self.id}')
                self.plc = mod.run
                self.plcGood = True
        else:
            print(f"Error: Controller {self.id} not in maintenance mode for PLC upload")

class WaysideIO(QWidget):
    def __init__(self, signals, logger):
        self.logger = logger
        self.logger.debug("Creating Wayside Controller")

        super().__init__()

        ## Signals
        self.signals = signals

        ## UI reference
        self.ui = None

        self.redlineTrack = None
        self.greenlineTrack = None

        self.lines = ['red', 'green']

        ## List for each controller
        self.redlineControllers = []
        self.greenlineControllers = []

        ## Block, Switch, Crossing lookup tables
        self.lookupTable = {
            'red' : {},
            'green' : {}
        }

    ###############
    ## CALLBACKS ##
    ###############
    def blockOccupancyCallback(self, occupancy):
        for i, block in enumerate(occupancy):
            self.setBlockOccupancy('green', i+1, block)

    def blockFailureCallback(self, blockFailures):
        if len(blockFailures) == 150:
            for i, failure in enumerate(blockFailures):
                self.setFaults('green', i+1, failure)
        else:
            for i, failure in enumerate(blockFailures):
                self.setFaults('red', i+1, failure)

    def filterSpeed(self, line, blockNum, speed):
        if int(self.lookupTable[line.lower()][str(blockNum)]['speed-limit']) < speed:
            return self.lookupTable[line.lower()][str(blockNum)]['speed-limit']
        else:
            return speed

    #############
    ## SETTERS ##
    #############
    def setFaults(self, line, blockNum, failures):
        if self.lines[0] == line.lower():
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            for c in controllers:
                self.redlineControllers[c[0]].updateFailures(blockNum, failures)

        if self.lines[1] == line.lower():
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            for c in controllers:
                self.greenlineControllers[c[0]].updateFailures(blockNum, failures)

    def setBlockOccupancy(self, line, blockNum, state):
        if self.lines[0] == line.lower():
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            for c in controllers:
                self.redlineControllers[c[0]].updateOccupancy(blockNum, state)

        if self.lines[1] == line.lower():
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            for c in controllers:
                self.greenlineControllers[c[0]].updateOccupancy(blockNum, state)

    def setBlockMaintenance(self, line, blockNum, state):
        if self.lines[0] == line.lower():
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            for c in controllers:
                self.redlineControllers[c[0]].updateMaintenance(blockNum, state)

        if self.lines[1] == line.lower():
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            for c in controllers:
                self.greenlineControllers[c[0]].updateMaintenance(blockNum, state)

    def setSwitch(self, line, blockNum, state):
        if self.lines[0] == line.lower():
            self.signals.switchState.emit([int(blockNum), state])
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            # for c in controllers:
                # self.redline_controllers[c[0]].updateSwitch(blockNum, state)

        if self.lines[1] == line.lower():
            self.signals.switchState.emit([int(blockNum), state])
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            # for c in controllers:
                # self.greenline_controllers[c[0]].updateSwitch(blockNum, state)

    def setCrossing(self, line, blockNum, state):
        if self.lines[0] == line.lower():
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            # for c in controllers:
            #     self.redline_controllers[c[0]].updateCrossing(blockNum, state)

        if self.lines[1] == line.lower():
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            # for c in controllers:
            #     self.greenline_controllers[c[0]].updateCrossing(blockNum, state)

    #############
    ## HELPERS ##
    #############
    ## Lookup table
    def lookupBlock(self, line, blockNum):
        return self.lookupTable[line.lower()][str(blockNum)]

    def uploadPLC(self, line, controllerNum, file):
        ## Redline
        if line.lower() == self.lines[0]:
            self.redlineControllers[controllerNum].uploadPLC(file)

        ## Greenline
        if line.lower() == self.lines[1]:
            self.greenlineControllers[controllerNum].uploadPLC(file)

    def populateTable(self, i, c, line):
        idx = 0
        for sec in c['sections']:
            for block in c['sections'][sec]['blocks']:
                entry = self.lookupTable[self.lines[line]]
                if block[0] not in entry:
                    entry[block[0]] = {
                        'controller' : [],
                    }
                ## Mapped data for a block
                entry[block[0]]['controller'].append((i,idx))
                entry[block[0]]['section'] = sec
                entry[block[0]]['speed-limit'] = block[1]
                idx+=1

    ###########
    ## SETUP ##
    ###########
    ## Setting a UI reference
    def setUI(self, ui):
        self.ui = ui

    ## Setting up the configuration for the redline
    def setupLine(self, line, layout, track):
        ## Redline
        if line.lower() == self.lines[0]:
            self.redlineTrack = track
            for i, c in enumerate(layout):
                self.redlineControllers.append(Controller(line.lower(), i, c, self.ui, self))
                self.populateTable(i, c, 0)

        ## Greenline
        if line.lower() == self.lines[1]:
            self.greenlineTrack = track
            for i, c in enumerate(layout):
                self.greenlineControllers.append(Controller(line.lower(), i, c, self.ui, self))
                self.populateTable(i,c, 1)

        ## Registering signal callbacks
        self.signals.blockFailures.connect(self.blockFailureCallback)
        self.signals.globalOccupancyFromTrackModelSignal.connect(self.blockOccupancyCallback)

if __name__ == '__main__':
    w = WaysideIO(1)

    csvPath = os.path.abspath(__file__)
    jsonPath = os.path.abspath(__file__)

    if os.name == 'nt':
        csvPath += "\\track_layout\\Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
        jsonPath += "\\track_layout\\greenline-layout.json"
    elif os.name == 'posix':
        csvPath += "/track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
        jsonPath += "/track_layout/greenline-layout.json"

    *other, layout = extract_layout.parseTrackLayout(csvPath, jsonPath)
    w.setupLine('green', layout)



