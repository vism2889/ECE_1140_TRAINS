#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: LayoutParserTest.py
# DESCRIPTION:
#       Code parse a rail system track layout file and storing the information
#   in BlockModel objects that can be passed to the TrackModelUI.py file.
#
##############################################################################

# IMPORTS
import csv
from re import I
from Block import Block
from BlockDictionary import BlockDictionary

class LayoutParserCTC:

    def __init__(self, pLayoutFile):
        self.filename  = pLayoutFile
        self.fields    = [] # Column Names
        self.rows      = [] # Data Rows / Block Information
        self.lineNames = [] # Names of all lines for a layout EX: [RED, GREEN]
        self.lines     = [] # List of list's len of self.lineNames, holding BlockModel objects for each line

    def process(self):
        with open(self.filename, 'r') as csvfile:
            csvreader   = csv.reader(csvfile)
            self.fields = next(csvreader)
            for row in csvreader:
                self.rows.append(row)

        self.lineNames = set()
        for row in self.rows:
            self.lineNames.add(row[0])
        self.lineNames = list(self.lineNames)

        self.redLineBlockDict = BlockDictionary()
        self.greenLineBlockDict = BlockDictionary()

        for i in range(len(self.lineNames)):
            self.lines.append([])

        for row in self.rows:
            block = Block(row[0], row[1], row[2],
                            row[3], row[5], row[6])
            if row[0] =="Red":
                self.redLineBlockDict.addBlock(block)
            elif row[0] =="Green":
                self.greenLineBlockDict.addBlock(block)

        return self.redLineBlockDict, self.greenLineBlockDict

def main():
    vLayout = "Track_Layout_PGH_Light_Rail.csv"
    parser = LayoutParser(vLayout)
    lines = parser.process()
    parser.printExampleBlock()

if __name__ == "__main__":
    main()