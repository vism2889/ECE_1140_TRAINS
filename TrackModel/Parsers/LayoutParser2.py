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

# Python IMPORTS
import csv
import sys

# Dependency Path Links
sys.path.insert(0,"..\Track-System-Models")

# Developer Imports
from BlockModel import BlockModel
from TrackSection import TrackSection
from TrackLine import TrackLine

class LayoutParser:
    '''
    Description Here
    '''

    def __init__(self, pLayoutFile):
        '''
        Description Here
        '''
        self.filename       = pLayoutFile
        self.fields         = [] # Column Names
        self.rows           = [] # Data Rows / Block Information
        
        self.trackLines     = [] 
        self.trackLineNames = [] # Names of all lines for a layout EX: [RED, GREEN]
        self.currTrackLine  = ""

        self.sections       = []
        self.sectionNames   = [] # Names of all the sections, of all the track lines
        self.currSection    = ""

        self.blocks         = []
        self.blockNames     = [] # Names of all the blocks, of all the sections, of all the trackLines

    def process(self):
        '''
        Description Here
        '''
        with open(self.filename, 'r') as csvfile:
            # print("\tParsing Track Layout File: ", self.filename)
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
        '''
        Description Here
        '''
        for trackLine in self.trackLines:
            print("Track Line:", trackLine.name)
            print("Number Sections:", len(trackLine.sections))
            for section in trackLine.sections:
                print(section.name)
                for block in section.blocks:
                    print("\t",block.blockNumber, block.section, "Underground:", block.underground, "Station:", block.station, "Switch:",block.switch)

    def addTrackLine(self, currTrackLineName):
        '''
        Description Here
        '''
        self.trackLineNames.append(currTrackLineName)
        self.currTrackLine = TrackLine(currTrackLineName)
        self.trackLines.append(self.currTrackLine)
        self.addSections()

    def updateTrackLine(self, currTrackLine):
        '''
        Description Here
        '''
        self.addSections()
        return 42

    def addSections(self):
        '''
        Description Here
        '''
        for row in self.rows:
            currSectionName = row[1]
            if currSectionName not in self.currTrackLine.sectionNames and self.currTrackLine.name == row[0]:
                self.addSection(currSectionName)
            else:
                continue

    def addSection(self, currSectionName):
        '''
        Description Here
        '''
        self.currTrackLine.sectionNames.append(currSectionName)
        self.currSection = TrackSection(currSectionName)
        self.currTrackLine.sections.append(self.currSection)
        self.addBlocks()

    def addBlocks(self):
        '''
        Description Here
        '''
        for row in self.rows:
            currBlockName = row[2]
            if currBlockName not in self.currSection.blockNames and self.currSection.name == row[1] and self.currTrackLine.name == row[0]:
                self.addBlock(currBlockName, row)

    def addBlock(self, currBlockName, row):
        '''
        Description Here
        '''
        self.currSection.blockNames.append(currBlockName)
        self.currBlock = BlockModel(row[0], row[1], row[2], row[3], 
                                    row[4], row[5], row[6], row[7], 
                                    row[8], row[9], row[10], row[11], 
                                    row[12], row[13]
                                    )
        self.parseInfrastructure()
        self.currSection.blocks.append(self.currBlock)
    
    def parseInfrastructure(self):
        '''
        Description Here
        '''
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
                
                newSwitch = []
                if len(switch) > 1:
                    switch = switch[1:]
                    if len(switch) > 2:
                        switch = switch[:2]
                    for item in switch:
                        x = item.strip("(")
                        x = x.replace(';', ' ')
                        
                        x = x.replace(")", '')
                        x = x.lstrip()
                        x = x.rstrip()
                        if ' ' in x:
                            x = x.split(' ')
                            for val in x:
                                newSwitch.append(val)
                        else:
                            newSwitch.append(x)
                        #print('item', x)
                # print('SWITCH', newSwitch)
                switch = newSwitch
                if len(switch) > 1 and type(switch)==list:
                    self.currBlock.switchForward = switch[0]
                    self.currBlock.switchReverse = switch[1]
                else:
                    self.currBlock.switchForward = switch
                self.currBlock.switch = switch
                # print("switch:      ", switch)
                if type(self.currBlock.switchForward) ==list:
                    self.currBlock.switchForward = self.currBlock.switchForward[0]
                self.currBlock.switchState = 'FORWARD'
                # print('forward', self.currBlock.switchForward)
                
                # print('reverse', self.currBlock.switchReverse)

            # else:
            #     switch = switch[0]
            #     self.currBlock.switch = switch
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