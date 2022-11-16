#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackSection.py
# DESCRIPTION:
#       Code for the Track Sections that make up the Track Model 
#
##############################################################################

class TrackSection:
    '''
    Class Description here
    '''
    def __init__(self, pName):
        self.name       = pName
        self.blocks     = []
        self.blockNames = []
        self.stations   = []
        self.switches   = []
        self.crossings  = []

    def __str__(self):
        return "Track Section: " + str(self.name) + "- contains " + str(len(self.blocks)) + " blocks"