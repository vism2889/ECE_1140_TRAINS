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
 
class LayoutParser:
    
    def __init__(self, pLayoutFile):
        self.filename  = pLayoutFile
        self.fields    = [] # Column Names
        self.rows      = [] # Data Rows / Block Information
        self.lineNames = [] # Names of all lines for a layout EX: [RED, GREEN]
        self.lines     = [] # List of list's len of self.lineNames, holding BlockModel objects for each line

    def process(self):
        print("\n\tPITTSBURGH LIGHT RAIL TRACK-LAYOUT PARSER")
        print("\t*****************************************")
        with open(self.filename, 'r') as csvfile:
            print("\tParsing Track Layout File: ", self.filename)
            csvreader   = csv.reader(csvfile)
            self.fields = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
            print("\tFile Parsing Complete\n")
            print("\t\tTotal no. of rows: %d"%(csvreader.line_num))
        
        print('\t\tField names are:')
        print('\t\t\t->',', '.join(field for field in self.fields))
        print("\t\tThe number of Track Blocks are: ", len(self.rows))
        print("\t\tExample data:")
        print("\t\t\t-> Row1 = ", self.rows[0])

        self.lineNames = set()
        for row in self.rows:
            self.lineNames.add(row[0])
        self.lineNames = list(self.lineNames)
        print("\t\tThere are", len(self.lineNames), "rail lines in this layout")
        print("\t\t\t-> Lines:", self.lineNames)

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

        print("\t\tThe Red line has", str(self.redLineBlockDict.len()), "blocks.")
        print("\t\tThe Green line has", str(self.greenLineBlockDict.len()), "blocks.")

        return self.redLineBlockDict, self.greenLineBlockDict
    
    def printExampleBlock(self):
        # Prints out all information for one the first block
        print("\t\tExample Block from Row1:",
                "\n\t\t\tLine: ", 
                self.rows[0][0], 
                "\n\t\t\tSection: ",
                self.rows[0][1],
                "\n\t\t\tBlock Number: ",
                self.rows[0][2],
                "\n\t\t\tBlock Length: ",
                self.rows[0][3],
                "\n\t\t\tBlock Grade: ",
                self.rows[0][4],
                "\n\t\t\tSpeed Limit: ",
                self.rows[0][5],
                "\n\t\t\tInfrastructure: ",
                self.rows[0][6],
                "\n\t\t\tStation Side: ",
                self.rows[0][7],
                "\n\t\t\tElevation: ",
                self.rows[0][8],
                "\n\t\t\tCummulative Elevation: ",
                self.rows[0][9],
                "\n\t\t\tSeconds to Traverse Block: ",
                self.rows[0][10])
        print("\n\tLAYOUT PARSER FINSIHED")

def main():
    vLayout = "Track_Layout_PGH_Light_Rail.csv"
    parser = LayoutParser(vLayout)
    lines = parser.process()
    parser.printExampleBlock()
    

if __name__ == "__main__":
    main()