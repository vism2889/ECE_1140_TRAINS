#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: InfraParser.py
# DESCRIPTION:
#       Code to test parsing the infrastructure column of the trackLayout.csv file.
#   This consists of blocks with stations and switches, along with underground blocks.
#
# TODO: 
#   Parse for underground sections.
#   Clean up switch parsing.
##############################################################################

import csv
class InfraParser:
    def __init__(self, pLayoutFile):
        self.filename = "Track_Layout_PGH_Light_Rail.csv"
        self.fields   = [] # Column Names
        self.rows     = [] # Data Rows / Block Information

        # list of stations - a list of objects holding the station name and the block number of that station
        self.stations = []

        # list of switches - a list of objects holding the blocknumber then a list of switch connections
        self.switches = []

        # list of underground blocks - a list of the blocks that are under ground
        self.underground = []

    def parse(self):
        print("\n\tPITTSBURGH LIGHT RAIL TRACK-LAYOUT INFRASTRUCTURE TEST PARSER")
        print("\t*****************************************")
        with open(self.filename, 'r') as csvfile:
            print("\tParsing Track Layout File: ", self.filename)
            csvreader = csv.reader(csvfile)
            self.fields    = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
            print("\tFile Parsing Complete\n")
            print("\t\tTotal no. of rows: %d"%(csvreader.line_num))

    def process(self):
        print("\t\tParsing for Stations and Switches")
        for row in self.rows:
            if row[6] != '':
                stationObj  =  ['','',''] #[station-name, block-number, underground]
                if 'STATION' in row[6]:
                    station = row[6].split()
                    if len(station) > 1:
                        station = station[1].strip(';')
                    else:
                        station = station[0]
                    block = row[2]
                    line = row[0]
                    self.stations.append([line, station, block])
                if 'SWITCH' in row[6]:
                    switch = row[6].split()
                    if len(switch) > 1:
                        switch = switch[1:]
                    else:
                        switch = switch[0]
                    block = row[2]
                    self.switches.append([switch, block])

        print("\t\tSTATIONS:")
        for stat in self.stations:
            print("\t\t ->",stat)

        print("\t\tSWITCHES:")
        for swit in self.switches:
            print("\t\t ->",swit)

if __name__ == '__main__':
    parser = InfraParser("dummyFileName")
    parser.parse()
    parser.process()