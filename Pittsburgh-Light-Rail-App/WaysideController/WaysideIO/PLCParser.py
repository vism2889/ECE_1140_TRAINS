import os
import re
import sys
from copy import deepcopy

class PLCParser():
    def __init__(self, controllerId):

        self.VAR_TYPES = ['#block_', '#switch_', '#crossing_']

        dir = None
        if os.name == 'posix':
            dir = '/plc'
        elif os.name == 'nt':
            dir = '\\plc'

        plcDir = os.path.join(os.getcwd() + dir) if dir != None else None

        if plcDir != None and not os.path.exists(plcDir):
            os.mkdir(plcDir)

        self.outfilePath = ""
        self.outfileName = ""
        if os.name == 'posix':
            self.outfilePath = os.getcwd() + f'{dir}/controller_plc_{controllerId}.py'
            self.outfileName = f"controller_plc_{controllerId}"
        elif os.name == 'nt':
            self.outfilePath = os.getcwd() + f'{dir}\\controller_plc_{controllerId}.py'
            self.outfileName = f"controller_plc_{controllerId}"

    def parseFile(self, file):

        outfile = open(self.outfilePath, 'w')
        tab = "\t"
        lines = []

        for line in file:
            for vtype in self.VAR_TYPES:
                idx = line.find(vtype)
                while idx>=0:
                    num = line[idx:].split(' ')[0].replace(vtype, '')
                    line = line.replace(vtype+num, f"input['{vtype.replace('#', '').replace(f'_', '')}']['{num}']")
                    idx = line.find(vtype)
            lines.append(tab + line)

        outfile.write("def run(input, running):\n")

        for l in lines:
            outfile.write(l + "\n")

        outfile.close()
        return self.outfileName


if __name__ == '__main__':

    parser = PLCParser(1)
    path = os.getcwd()

    if os.name == 'nt':
        path += "\\tests\\testplc.plc"
    elif os.name == 'posix':
        path += "/tests/testplc.plc"

    file = open(path, 'r')
    parser.parseFile(file)
    file.close()