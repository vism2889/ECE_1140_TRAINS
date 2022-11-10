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

        if os.name == 'posix':
            self.outfilePath = os.getcwd() + f'{dir}/controller_plc_{controllerId}.py'
        elif os.name == 'nt':
            self.outfilePath = os.getcwd() + f'{dir}\\controller_plc_{controllerId}.py'

    def parseFile(self, file):

        outfile = open(self.outfilePath, 'w')
        lines = []

        for line in file:
            for vtype in self.VAR_TYPES:
                idx = line.find(vtype)
                while idx>=0:
                    num = line[idx:].split(' ')[0].replace(vtype, '')
                    line = line.replace(vtype+num, f"input['{vtype.replace('#', '').replace(f'_', '')}']['{num}']")
                    idx = line.find(vtype)
            lines.append(line)

        print(lines)

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