import os
from PLCParser import PLCParser
import importlib

## testing
from track_layout import extract_layout

class Controller:
    def __init__(self, controllerNum, layout):

        self.layout = layout
        ## Function to run PLC program
        self.plc = None
        self.plcGood = False

        ##
        self.maintenance = True

        ## Setup layout
        self.track = {
            'blocks' : {},
            'switches' : {},
            'crossings': {},
            'failures' : {}
        }

        for section in self.layout['sections']:
            ## Blocks
            for block in self.layout['sections'][section]['blocks']:
                self.track['blocks'][block[0]] = block[1]

            ## Switches
            for switch in self.layout['sections'][section]['switches']:
                self.track['switches'][switch] = False

            ## Crossings
            for crossing in self.layout['sections'][section]['crossing']:
                self.track['crossings'][crossing] = False

        self.id = controllerNum
        self.parser = PLCParser(controllerNum)


    ## Get Current Track State ##
    def getStates(self):
        return self.track

    ## Update block occupancies
    def updateStates(self, blocks):
        for i,block in enumerate(blocks):
            self.track['blocks'][i] = block

    ## Run the PLCs ##
    def run(self):
        if self.plcGood:
            try:
                self.plc(self.track)
            except:
                self.plcGood = False
            else:
                ## TODO Send data out 
                pass

    ## Toggle maintenance mode ##
    def toggleMaintence(self):
        self.maintenance != self.maintenance
        return self.maintenance

    ## Upload a PLC ##
    def uploadPLC(self, file):
        if self.maintenance:
            modname = self.parser.parseFile(file)
            try:
                mod = importlib.import_module("plc."+modname)
            except ImportError:
                print("Err in importing PLC program")
                self.plcGood = False
            else:
                self.plc = mod.run
                self.plcGood = True
        else:
            print(f"Error: Controller {self.id} not in maintenance mode for PLC upload")

    ## Filter Authority ## 
    def filterAuthority(self, blockNum, authority):
        if self.track['blocks'][blockNum] 

class WaysideIO:
    def __init__(self, ui):

        self.track = {}
        self.blockStates = []

        self.lines = ['red', 'green']

        ## Hold each controller
        self.redline_controllers = []
        self.greenline_controllers = []

        ## Block, Switch, Crossing lookup tables
        self.lookupTable = {
            'red' : {},
            'green' : {}
        }

    def filterSpeed(self, line, blockNum, speed):
        if int(self.lookupTable[line.lower()][str(blockNum)]['speed-limit']) < speed:
            return self.lookupTable[line.lower()][str(blockNum)]['speed-limit']
        else:
            return speed

    def lookupBlock(self, line, blockNum):
        return self.lookupTable[line.lower()][str(blockNum)]

    def uploadPLC(self, line, controllerNum, file):
        ## Redline
        if line.lower() == self.lines[0]:
            self.redline_controllers[controllerNum].uploadPLC(file)

        ## Greenline
        if line.lower() == self.lines[1]:
            self.greenline_controllers[controllerNum].uploadPLC(file)


    def setupLine(self, line, layout):
        ## Redline
        if line.lower() == self.lines[0]:
            for i, c in enumerate(layout):
                self.redline_controllers.append(Controller(i, c))

                ## Populate lookup table
                for sec in c['sections']:
                    for block in c['sections'][sec]['blocks']:
                        entry = self.lookupTable[self.lines[0]]
                        if block[0] not in entry:
                            entry[block[0]] = {
                                'controller' : [],
                            }

                        ## Mapped data for a block
                        entry[block[0]]['controller'].append(i)
                        entry[block[0]]['section'] = sec
                        entry[block[0]]['speed-limit'] = block[1]

        ## Greenline
        if line.lower() == self.lines[1]:
            for i, c in enumerate(layout):
                self.greenline_controllers.append(Controller(i, c))

                ## Populate lookup table
                for sec in c['sections']:
                    for block in c['sections'][sec]['blocks']:

                        blockData = c['sections'][sec]['blocks']
                        entry = self.lookupTable[self.lines[1]]
                        if block[0] not in entry:
                            entry[block[0]] = {
                                'controller' : [],
                            }

                        ## Mapped data for a block
                        entry[block[0]]['controller'].append(i)
                        entry[block[0]]['section'] = sec
                        entry[block[0]]['speed-limit'] = block[1]

if __name__ == '__main__':
    w = WaysideIO(1)

    ## Testing PLC parsing
    # f = open('tests/testplc.plc', 'r')
    # w.uploadPLC(f)

    ## Testing configuration
    csvPath = os.getcwd()
    jsonPath = os.getcwd()

    if os.name == 'nt':
        csvPath += "\\track_layout\\Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
        jsonPath += "\\track_layout\\greenline-layout.json"
    elif os.name == 'posix':
        csvPath += "/track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
        jsonPath += "/track_layout/greenline-layout.json"

    *other, layout = extract_layout.parseTrackLayout(csvPath, jsonPath)
    w.setupLine('green', layout)


    ## Testing filter speed
    # print(w.filterSpeed('green', 1, 105))


