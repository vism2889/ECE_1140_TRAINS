import os
import sys
import importlib
sys.path.append('/track_layout')

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
        self.plcGood = False

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
                self.track['block'][int(block[0])] = block[2]
                self.track['block-states'][int(block[0])] = 0x00
                self.numBlocks+=1

            ## Switches
            for switch in self.layout['sections'][section]['switches']:
                self.track['switch'][int(switch)] = True

            ## Crossings
            for crossing in self.layout['sections'][section]['crossing']:
                self.track['crossing'][int(crossing)] = False

        self.id = controllerNum

        ## Initalizing track component values
        self.updateCrossing()
        self.updateSwitch()

        ## Setup PLC interface
        self.parser = PLCParser(controllerNum, self.line)

        ## Load the default PLC programs
        file = open(f"plc/{self.line}/{self.line}line_controller{self.id}.plc")
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
        self.track['block'][blockNum] = state
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
        self.maintenance = state
        ## Plubish maintenance state
        if self.line == 'red':
            self.parent.publishMaintenance(0, blockNum, state)
        if self.line == 'green':
            self.parent.publishMaintenance(1, blockNum, state)

        # if state == True:
        #     self.maintenance = True
        #     return

        # print(f'state: {state}')
        # for block in self.track['block-maintenance']:
        #     if self.track['block-maintenance'][block] == True:
        #         self.maintenance = True
        #         return

        # self.maintenance = state
        return

    ## Switches and crossing only get update with the PLC program
    def updateSwitch(self):
        for switch in self.track['switch']:
            self.parent.setSwitch(self.line, int(switch), self.track['switch'][switch])
            self.ui.setSwitchState(self.line, int(switch), self.track['switch'][switch])

        return self.track['switch']

    ## Updates the crossing state of the controller
    def updateCrossing(self):
        for crossing in self.track['crossing']:
            self.parent.setCrossing(self.line, crossing, self.track['crossing'][crossing])
            self.ui.setCrossingState(self.line, int(crossing), self.track['crossing'][crossing])

        ## Run PLC program
        return self.track['crossing']

    ## Manually setting switches
    def setSwitch(self, blockNum, state):
        if blockNum not in self.track['block-maintenance']:
            print("err in setting switch")
            return -1

        if self.track['block-maintenance'][blockNum]:
            self.track['switch'][blockNum] = state
            self.updateSwitch()

    ## Run the PLCs
    def run(self):
        if self.plcGood and not self.maintenance:
            try:
                self.plc.run(self.track)
            except:
                # print(e)
                print(f'Error: PLC script cannot run ({self.line}controller{self.id})')
                self.plcGood = False

    ## Upload a PLC
    def uploadPLC(self, file):
        # print(f'func: {self.maintenance}')
        if self.maintenance:
            modname = self.parser.parseFile(file)
            try:
                if self.plc == None:
                    self.plc = importlib.import_module(f"plc.{self.line}."+modname)
                else:
                    importlib.reload(self.plc)
            except ImportError:
                print(f"Errror: Could not import plc script for {self.line}line controller {self.id}")
                self.plcGood = False
            else:
                self.plc.run(self.track)
                self.plcGood = True
        else:
            print(f"Error: Controller {self.id} not in maintenance mode for PLC upload")

    ## Return if a block, in maintenance or has  fault
    def blockState(self, blockNum):
        flag = 0
        if self.track['block'][blockNum]:
            flag +=1
        if self.track['block-states'][blockNum]:
            flag +=1

        if blockNum in self.track['block-maintenance']:
            if self.track['block-maintenance'][blockNum]:
                flag += 1

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

        self.activeTrains = {
            0 : {}, ## Red
            1 : {} ## Green
        }


    ###############
    ## CALLBACKS ##
    ###############
    def suggestSpeed(self, msg):
        if msg[1] == 'Red Line':
            self.activeTrains[0][msg[0]] = [None, msg[2]*3.6]
        if msg[1] == 'Green Line':
            self.activeTrains[1][msg[0]] = [None, msg[2]*3.6]

        # if msg[0] not in self.activeTrains[0]:
        #     self.activeTrains[0][msg[0]] = [None, msg[1]]

        # if msg[0] not in self.activeTrains[1]:
        #     self.activeTrains[1][msg[0]] = [None, msg[1]]

    ## Train Location callback that determines authority
    def trainLocationCallback(self, loc):
        if len(loc) != 4:
            return

        ## Figure out what line its
        line = loc[0]
        id = loc[1] ## train id
        prev = loc[2]
        curr = loc[3]

        speed = 0

        ## Save train location for speed
        if id in self.activeTrains[line]:
            self.activeTrains[line][id][0] = curr

            if line == 0:
                speedLim = self.redlineTrack.getBlock(curr).speedLimit
            if line == 1:
                speedLim = self.greenlineTrack.getBlock(curr).speedLimit

            if self.activeTrains[line][id][1] > int(speedLim):
                speed = int(speedLim)
            else:
                speed = self.activeTrains[line][id][1]
        else:
            if line == 0:
                self.activeTrains[line][id] = [curr, int(self.redlineTrack.getBlock(curr).speedLimit)]
            if line == 1:
                self.activeTrains[line][id] = [curr, int(self.greenlineTrack.getBlock(curr).speedLimit)]

        # print(f'({line}) :\ttrain id {id}, speed {speed/1.60934}, block {curr}')
        self.signals.regulatedSpeed.emit([line, id, speed])

        if line == 0:
            authority= self.planAuthority('red', self.redlineControllers, self.redlineTrack, curr, prev)
            self.signals.waysideAuthority.emit([0, id, authority])

        if line == 1:
            authority = self.planAuthority('green', self.greenlineControllers, self.greenlineTrack, curr, prev)
            self.signals.waysideAuthority.emit([1, id, authority])

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

    def blockFailureCallback(self, msg):
        ## Extract the individual faults
        for i, failure in enumerate(msg[0]):
            self.setFaults('red', i+1, failure)

        for i, failure in enumerate(msg[1]):
            self.setFaults('green', i+1, failure)

    def maintenanceCallback(self, msg):
        if msg[0] == 0:
            self.setBlockMaintenance('red', msg[1], msg[2])
        if msg[0] == 1:
            self.setBlockMaintenance('green', msg[1], msg[2])

    def publishMaintenance(self, line, block, state):
        self.signals.blockMaintenance.emit([line, block, state])

    def ctcSetSwitch(self, msg):
        blockNum = msg[1]
        state = msg[2]

        ## Redline
        if msg[0] == 0:
            controllers = self.lookupBlock('red', blockNum)['controller']
            for c in controllers:
                self.redlineControllers[c[0]].setSwitch(blockNum, state)

        ## Greenline
        if msg[0] == 1:
            controllers = self.lookupBlock('green', blockNum)['controller']
            for c in controllers:
                self.greenlineControllers[c[0]].setSwitch(blockNum, state)

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
        controllers = self.lookupBlock(line, blockNum)['controller']
        # print(self.redlineControllers)
        ## redline
        if self.lines[0] == line.lower():
            self.signals.switchState.emit([0, int(blockNum), state])
            res = self.redlineTrack.setSwitch(int(blockNum), state)

            for c in controllers:
                if len(self.redlineControllers) > c[0]:
                    self.redlineControllers[c[0]].track['switch'][blockNum] = state

        ## greenline
        if self.lines[1] == line.lower():
            self.signals.switchState.emit([1, int(blockNum), state])
            res = self.greenlineTrack.setSwitch(int(blockNum), state)
            for c in controllers:
                if len(self.greenlineControllers) > c[0]:
                    self.greenlineControllers[c[0]].track['switch'][blockNum] = state


    def setCrossing(self, line, blockNum, state):
        if self.lines[0] == line.lower():
            self.signals.crossingState.emit([0, int(blockNum), state])
            controllers = self.lookupBlock(self.lines[0], blockNum)['controller']
            # for c in controllers:
            #     self.redline_controllers[c[0]].updateCrossing(blockNum, state)

        if self.lines[1] == line.lower():
            self.signals.crossingState.emit([1, int(blockNum), state])
            controllers = self.lookupBlock(self.lines[1], blockNum)['controller']
            # for c in controllers:
            #     self.greenline_controllers[c[0]].updateCrossing(blockNum, state)

    #############
    ## GETTERS ##
    #############
    def getOccupancy(self, line, blockNum):
        occupied = True
        controllers = self.lookupBlock(line, blockNum)['controller']

        if line == 'red':
            for c in controllers:
                occupied &= self.redlineControllers[c[0]].blockState(blockNum)

        if line == 'green':
            for c in controllers:
                occupied &= self.greenlineControllers[c[0]].blockState(blockNum)

        return occupied

    #############
    ## HELPERS ##
    #############
    ## Figure out the next 1-5 blocks that are traversable
    def planAuthority(self, line, controllers, track, curr, prev):
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
                if len(authority) > 2:
                    authority.pop(-1)
                    authority.pop(-1)
                elif len(authority) > 1:
                    authority.pop(-1)
                return authority

            ## Check if it's the yard
            if nextBlock.id == 0:
                authority.append(nextBlock.id)
                return authority

            ## Check the state of the block
            controller = self.lookupBlock(line, nextBlock.id)['controller']
            blockOccupied = controllers[controller[0][0]].blockState(nextBlock.id)

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
                self.populateTable(i, c, 0)
                self.redlineControllers.append(Controller(line.lower(), i, c, self.ui, self))

        ## Greenline
        if line.lower() == self.lines[1]:
            self.greenlineTrack = track
            for i, c in enumerate(layout):
                self.populateTable(i,c, 1)
                self.greenlineControllers.append(Controller(line.lower(), i, c, self.ui, self))

        ## Registering signal callbacks
        self.signals.trackFailuresSignal.connect(self.blockFailureCallback)
        self.signals.globalOccupancyFromTrackModelSignal.connect(self.blockOccupancyCallback)
        self.signals.signalMaintenance.connect(self.maintenanceCallback)
        self.signals.trainLocation.connect(self.trainLocationCallback)
        self.signals.ctcSwitchState.connect(self.ctcSetSwitch)
        self.signals.dispatchTrainSignal.connect(self.suggestSpeed)

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



