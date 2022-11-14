import os
from PLCParser import PLCParser
import importlib

## testing
from track_layout import extract_layout

class Controller:
    def __init__(self, controllerNum, layout):

        ## Function to run PLC program
        self.plc = None
        self.plcGood = False

        self.parser = PLCParser(controllerNum)

    ## Run the PLCs
    def run(self):
        input = {
            'switch'
        }
        if self.plcGood:
            try:
                self.plc(self.track)
            except:
                self.plcGood = False

    ##
    def uploadPLC(self, file):
        modname = self.parser.parseFile(file)
        try:
            mod = importlib.import_module("plc."+modname)
        except ImportError:
            print("Err in importing PLC program")
            self.plcGood = False
        else:
            self.plc = mod.run
            self.plcGood = True

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

    def updateBlock(self,line, blockNum):
        pass

    def setupLine(self, line, layout):

        ## Redline
        if line.lower() == self.lines[0]:
            for i, c in enumerate(layout):
                self.redline_controllers.append(c)

                ## Populate lookup table
                for sec in c['sections']:
                    for block in c['sections'][sec]['blocks']:
                        entry = self.lookupTable[self.lines[0]]
                        if block[0] not in entry:
                            entry[block[0]] = {
                                'controller' : [],
                            }

                        entry[block[0]]['controller'].append(i)
                        entry[block[0]]['section'] = sec

        ## Greenline
        if line.lower() == self.lines[1]:
            for i, c in enumerate(layout):
                self.greenline_controllers.append(c)

                ## Populate lookup table
                for sec in c['sections']:
                    for block in c['sections'][sec]['blocks']:
                        entry = self.lookupTable[self.lines[1]]
                        if block[0] not in entry:
                            entry[block[0]] = {
                                'controller' : [],
                            }

                        entry[block[0]]['controller'].append(i)
                        entry[block[0]]['section'] = sec
        print(self.lookupTable)

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
