#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackLine.py
# DESCRIPTION:
#       Code for the Track Lines that make up the Track Model 
#
##############################################################################

class TrackLine:
    '''
    Class Description here
    '''
    def __init__(self, pName):
        self.name         = pName
        self.sections     = []
        self.blocks       = []
        self.sectionNames = []
        self.stations     = []
        self.switches     = []
        self.crossings    = []

    def __str__(self):
        return "Track Line: " + str(self.name) + "- contains " + str(len(self.sections)) + " sections"