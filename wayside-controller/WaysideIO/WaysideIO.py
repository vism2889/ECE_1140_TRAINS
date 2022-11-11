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

        ## Hold each controller
        self.redline_controllers = []
        self.greenline_controllers = []

    def setupLine(self, layout):

        lineName, controllers = layout

        ## Setup redline controllerss
        if lineName == 'redline':
            for i,c in enumerate(controllers):

                controller = {
                    'block' : {},
                    'switch' : {},
                    'crossing' : {}
                }

                ## Go through the blocks
                for blocks in c['block-occupancy']:
                    controller['block'][blocks[0]] = (blocks[2], blocks[3])

                ## Go through the switchs
                for switches in c['switch-state']:
                    controller['switch'][switches[0]] = switches[2]

                ## Go through the crossings
                for crossings in c['crossing-state']:
                    controller['crossing'][crossings[0]] = crossings[2]

                print(controller)
                self.redline_controllers.append(Controller(i, controller))


        print(self.redline_controllers)



if __name__ == '__main__':
    w = WaysideIO(1)

    ## Testing PLC parsing
    # f = open('tests/testplc.plc', 'r')
    # w.uploadPLC(f)

    path = os.getcwd()

    if os.name == 'nt':
        path += "\\track_layout\\Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
    elif os.name == 'posix':
        path += "/track_layout/Track Layout & Vehicle Data vF.xlsx - Green Line.csv"

    layout = extract_layout.parseTrackLayout(path)
    # print(layout)
    w.setupLine(('redline', layout))

