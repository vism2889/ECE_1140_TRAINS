import os
import sys
import importlib
sys.path.append('./extract_layout')

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

        ## Function to run PLC program
        self.plc = None
        self.plcGood = True

        ##
        self.maintenance = True
        self.numBlocks = 0

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
                self.numBlocks+=1

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

    ###############
    ## BLOCK OPS ##
    ###############
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
        # if failures!= 0x00:
        #     print(f'Updating failures for line {self.line} and block {blockNum}')
        self.track['block-states'][blockNum] = failures

        ## Extract the individual faults
        faults = []

        ## Track Failure (0x01)
        if 0x01 & failures:
            faults.append(1)
        ## Circuit Failure
        if 0x02 & failures:
            faults.append(2)
        ## Power Failure
        if 0x04 & failures:
            faults.append(3)

        self.parent.ui.setFaultState(self.line, blockNum, faults)
        return self.track['block-states']

    ## Updates the controller maintenance state
    def updateMaintenance(self, blockNum, state):
        self.track['block-maintenance'][blockNum] = state
        self.parent.ui.setMaintenance(self.line, blockNum, state)
        return self.track['block-maintenance']

    ## Switches and crossing only get update with the PLC program
    def updateSwitch(self):
        for switch in self.track['switch']:
            self.parent.setSwitch(self.line, switch, self.track['switch'][switch])
            self.ui.setSwitchState(self.line, int(switch), self.track['switch'][switch])

        return self.track['switch']

    ## Updates the crossing state of the controller
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
                self.plc = mod.run
                self.plcGood = True
        else:
            print(f"Error: Controller {self.id} not in maintenance mode for PLC upload")

    ## Return if a block, in maintenance or has  fault
    def blockState(self, blockNum):
        flag = 0

        if self.track['block'][str(blockNum)]:
            flag +=1
        if self.track['block-states'][str(blockNum)]:
            flag +=1

        return flag

class WaysideIO(QWidget):
    def __init__(self, signals):
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

        self.test = False

    ###############
    ## CALLBACKS ##
    ###############
    ## Train Location callback that determines authority
    def trainLocationCallback(self, loc):
        if len(loc) != 4:
            return

        ## Figure out what line its
        line = loc[0]
        id = loc[1] ## train id
        prev = loc[2]
        curr = loc[3]

        if line.lower() == 'red':
            controllers = self.lookupTable[line.lower()][str(curr)]['controller']
            authority = self.planAuthority(self.redlineControllers[controllers[0][0]], self.redlineTrack, curr, prev)
            self.signals.waysideAuthority.emit([line.lower(), id, authority])

        if line.lower() == 'green':
            controllers = self.lookupTable[line.lower()][str(curr)]['controller']
            authority = self.planAuthority(self.greenlineControllers[controllers[0][0]], self.greenlineTrack, curr, prev)
            self.signals.waysideAuthority.emit([line.lower(), id, authority])

    ##  Driver for most of the logic
    #       Sets block occupancy and eventually runs
    #       the PLC program loaded into the controller
    def blockOccupancyCallback(self, occupancy):
        redLine = occupancy[0]
        greenLine = occupancy[1]

        for i, block in enumerate(redLine):
            self.setBlockOccupancy('red', i+1, block)

        for i, block in enumerate(greenLine):
            self.setBlockOccupancy('green', i+1, block)

    def blockFailureCallback(self, failures):
        if not self.test:
            ## Extract the individual faults
            if len(failures) == 150:
                for i, failure in enumerate(failures):
                    self.setFaults('green', i+1, failure)
            else:
                for i, failure in enumerate(failures):
                    self.setFaults('red', i+1, failure)

    def maintenanceCallback(self, msg):
        self.setBlockMaintenance(msg[0], msg[1], [msg[2]])

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
        ## redline
        if self.lines[0] == line.lower():
            self.signals.switchState.emit([int(blockNum), state])
            res = self.redlineTrack.setSwitch(int(blockNum), state)

        ## greenline
        if self.lines[1] == line.lower():
            self.signals.switchState.emit([int(blockNum), state])
            res = self.greenlineTrack.setSwitch(int(blockNum), state)

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

    ## Figure out the next 1-5 blocks that are traversable
    def planAuthority(self, controller, track, curr, prev):
        previousBlock = prev
        currentBlock = curr
        authority = [curr]

        ## Look at the next five blocks
        i = 0
        while i < 5:
            ## Get the next block
            nextBlock = track.getNextBlock(currentBlock, previousBlock)
            if nextBlock == -1:
                ## Set a 2 block buffer for the authority
                authority.pop(-1)
                authority.pop(-1)
                return authority

            ## Check the state of the block
            blockOccupied = controller.blockState(nextBlock.id)
            if not blockOccupied:
                authority.append(nextBlock.id)
            else:
                if len(authority) <= 2:
                    return [curr]

                ## Set a 2 block buffer for the authority
                authority.pop(-1)
                authority.pop(-1)
                return authority

            previousBlock = currentBlock
            currentBlock = nextBlock.id
            i+=1

        return authority

    def checkBlockState(self, line, blockNum):
        if line.lower() == 'red':
            controllerNum = self.lookupTable[line.lower()][str(blockNum)]
            # self.redlineControllers[controllerNum].
            pass

        if line.lower() == 'green':
            pass

    ## Get the number of blocks in a controller
    def getNumBlocks(self, line, controller):
        if line.lower() == 'red':
            return self.redlineControllers[controller].numBlocks
        if line.lower() == 'green':
            return self.greenlineControllers[controller].numBlocks
        return -1

    ## Lookup table (TODO) either keep this or remove it
    def lookupBlock(self, line, blockNum):
        return self.lookupTable[line.lower()][str(blockNum)]

    ## Set a controllers PLC program
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

        # print(self.lookupTable['red'][str(24)])

        ## Registering signal callbacks
        self.signals.blockFailures.connect(self.blockFailureCallback)
        self.signals.globalOccupancyFromTrackModelSignal.connect(self.blockOccupancyCallback)
        self.signals.signalMaintenance.connect(self.maintenanceCallback)
        self.signals.trainLocation.connect(self.trainLocationCallback)

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



