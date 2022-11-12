#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: LayoutParser.py
# DESCRIPTION:
#       Code parse a rail system track layout file and storing the information
#   in TrackLine, TrackSection, and BlockModel objects that can be passed to the 
#   TrackModelUI.py file.
#
##############################################################################

# IMPORTS
import csv
import sys
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from BlockModel import BlockModel
from TrackSection import TrackSection
from TrackLine import TrackLine

 
class LayoutParser:
    
    def __init__(self, pLayoutFile):
        self.filename       = pLayoutFile
        self.fields         = [] # Column Names
        self.rows           = [] # Data Rows / Block Information
        
        self.trackLines     = [] 
        self.trackLineNames = [] # Names of all lines for a layout EX: [RED, GREEN]
        self.currTrackLine = ""

        self.sections       = []
        self.sectionNames   = [] # Names of all the sections, of all the track lines
        self.currSection    = ""

        self.blocks         = []
        self.blockNames     = [] # Names of all the blocks, of all the sections, of all the trackLines

    def process(self):
        with open(self.filename, 'r') as csvfile:
            print("\tParsing Track Layout File: ", self.filename)
            csvreader   = csv.reader(csvfile)
            self.fields = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
        
        for row in self.rows:
            currTrackLineName = row[0]
            if currTrackLineName not in self.trackLineNames:
                self.addTrackLine(currTrackLineName)
            else:
                self.updateTrackLine(self.currTrackLine)
        return self.trackLines

    def displayData(self):
        for trackLine in self.trackLines:
            print("Track Line:", trackLine.name)
            print("Number Sections:", len(trackLine.sections))
            for section in trackLine.sections:
                print(section.name)
                for block in section.blocks:
                    print("\t",block.blockNumber, block.section, "Underground:", block.underground, "Station:", block.station, "Switch:",block.switch)

    def addTrackLine(self, currTrackLineName):
        self.trackLineNames.append(currTrackLineName)
        self.currTrackLine = TrackLine(currTrackLineName)
        self.trackLines.append(self.currTrackLine)
        self.addSections()

    def updateTrackLine(self, currTrackLine):
        self.addSections()
        return 42

    def addSections(self):
        for row in self.rows:
            currSectionName = row[1]
            if currSectionName not in self.currTrackLine.sectionNames and self.currTrackLine.name == row[0]:
                self.addSection(currSectionName)
            else:
                continue

    def addSection(self, currSectionName):
        self.currTrackLine.sectionNames.append(currSectionName)
        self.currSection = TrackSection(currSectionName)
        self.currTrackLine.sections.append(self.currSection)
        self.addBlocks()

    def addBlocks(self):
        for row in self.rows:
            currBlockName = row[2]
            if currBlockName not in self.currSection.blockNames and self.currSection.name == row[1] and self.currTrackLine.name == row[0]:
                self.addBlock(currBlockName, row)

    def addBlock(self, currBlockName, row):
        self.currSection.blockNames.append(currBlockName)
        self.currBlock = BlockModel(row[0], row[1], row[2], row[3], 
                                          row[4], row[5], row[6], row[7], 
                                          row[8], row[9], row[10]
                                          )
        self.parseInfrastructure()
        self.currSection.blocks.append(self.currBlock)
    
    def parseInfrastructure(self):
        infra = self.currBlock.infrastructure
        if infra != '':
            if 'STATION' in infra:
                station = infra.split()
                if len(station) > 1:
                    station = station[1].strip(';')
                    self.currBlock.station = station
                else:
                    station = station[0]
                    self.currBlock.station = station
            if 'SWITCH' in infra:
                switch = infra.split()
                if len(switch) > 1:
                    switch = switch[1:]
                    self.currBlock.switch = switch
                else:
                    switch = switch[0]
                    self.currBlock.switch = switch
            if 'CROSSING' in infra:
                self.currBlock.crossingPresence = True
            if 'UNDERGROUND' in infra:
                self.currBlock.underground = True

def main():
    vLayout = "../Layout-Files/Track_Layout_PGH_Light_Rail.csv"
    parser = LayoutParser(vLayout)
    parser.process()
    #parser.displayData()
    

if __name__ == "__main__":
    main()