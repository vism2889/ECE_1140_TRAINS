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
from BlockModel import BlockModel
from TrackSection import TrackSection
from TrackLine import TrackLine
 
class LayoutParser:
    
    def __init__(self, pLayoutFile):
        self.filename  = pLayoutFile
        self.fields    = [] # Column Names
        self.rows      = [] # Data Rows / Block Information
        self.trackLines = [] # Names of all lines for a layout EX: [RED, GREEN]
        self.trackLineNames =  []

    def process(self):
        # print("\n\tPITTSBURGH LIGHT RAIL TRACK-LAYOUT PARSER")
        # print("\t*****************************************")
        with open(self.filename, 'r') as csvfile:
            print("\tParsing Track Layout File: ", self.filename)
            csvreader   = csv.reader(csvfile)
            self.fields = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
            print("\tFile Parsing Complete\n")
            print("\t\tTotal no. of rows: %d"%(csvreader.line_num))
        
        # print('\t\tField names are:')
        # print('\t\t\t->',', '.join(field for field in self.fields))
        # print("\t\tThe number of Track Blocks are: ", len(self.rows))
        # print("\t\tExample data:")
        # print("\t\t\t-> Row1 = ", self.rows[0])

        for row in self.rows:
            if row[0] not in self.trackLines:
                currTrackLine = TrackLine(row[0])
                
                currSection   = TrackSection(row[1])
                currBlock     = BlockModel(row[0], row[1], row[2], row[3], 
                                          row[4], row[5], row[6], row[7], 
                                          row[8], row[9], row[10]
                                          )
                currSection.blocks.append(currBlock)
                currTrackLine.sections.append(currSection)
                self.trackLines.append(currTrackLine)
                currTrackLine.sections.append(currSection)
                curr
        self.trackLineNames = set()
        for row in self.rows:
            self.trackLineNames.add(row[0])
        self.trackLineNames = sorted(list(self.trackLineNames))
        print("\t\tThere are", len(self.trackLineNames), "rail lines in this layout")
        print("\t\t\t-> Lines:", self.trackLineNames)


        # Creates a list of TrackLine objects
        for line in self.trackLineNames:
            currTrackLine =  TrackLine(line)
            self.trackLines.append(currTrackLine)

        print(self.trackLineNames, self.trackLines)

        #print(self.rows[0])
        for i in range(len(self.trackLines)):
            sections = []#set()
            for row in self.rows:
                if row[0] == self.trackLines[i].name and row[1] not in sections:
                    sections.append(row[1])
                    currSection = TrackSection(row[1])
                    self.trackLines[i].sections.append(currSection)
            print(sections)
                
        # for line in self.trackLines:
        #     for sec in line.sections:
        #         print(line.name, sec)

        for row in self.rows:
            for line in self.trackLines:
                for sec in line.sections:
                    if row[1] == sec.name:
                        currBlock = BlockModel(row[0], row[1], row[2], row[3], 
                                        row[4], row[5], row[6], row[7], 
                                        row[8], row[9], row[10]
                                        )
                        sec.blocks.append(currBlock)

        for line in self.trackLines:
            print(len(line.sections))
            # for sec in line.sections:
            #     print("section:", sec.name, "\n", len(sec.blocks))

    #     for row in self.rows:
    #         for i in range(len(self.lineNames)):
    #             if row[0] == self.lineNames[i]:
                    # block = BlockModel(row[0], row[1], row[2], row[3], 
                    #                     row[4], row[5], row[6], row[7], 
                    #                     row[8], row[9], row[10])
    #                 self.lines[i].append(block)
    #                 blockCountPerLine[i]+=1

    #     for i in range(len(self.lineNames)):
    #         print("\t\tThe", self.lineNames[i], "line has", blockCountPerLine[i], "blocks.")

    #     return self.lineNames, self.lines
    
    # def printExampleBlock(self):
    #     # Prints out all information for one the first block
    #     print("\t\tExample Block from Row1:",
    #             "\n\t\t\tLine: ", 
    #             self.rows[0][0], 
    #             "\n\t\t\tSection: ",
    #             self.rows[0][1],
    #             "\n\t\t\tBlock Number: ",
    #             self.rows[0][2],
    #             "\n\t\t\tBlock Length: ",
    #             self.rows[0][3],
    #             "\n\t\t\tBlock Grade: ",
    #             self.rows[0][4],
    #             "\n\t\t\tSpeed Limit: ",
    #             self.rows[0][5],
    #             "\n\t\t\tInfrastructure: ",
    #             self.rows[0][6],
    #             "\n\t\t\tStation Side: ",
    #             self.rows[0][7],
    #             "\n\t\t\tElevation: ",
    #             self.rows[0][8],
    #             "\n\t\t\tCummulative Elevation: ",
    #             self.rows[0][9],
    #             "\n\t\t\tSeconds to Traverse Block: ",
    #             self.rows[0][10])
    #     print("\n\tLAYOUT PARSER FINSIHED")

def main():
    vLayout = "Track_Layout_PGH_Light_Rail.csv"
    parser = LayoutParser(vLayout)
    lines = parser.process()
    #parser.printExampleBlock()
    #print("\nLINE 1:\n",lines[0])
    #print("\nLINE 2:\n",lines[1])

if __name__ == "__main__":
    main()