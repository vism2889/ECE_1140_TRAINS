#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     09/30/2022
# FILENAME: TrackModel.py
# DESCRIPTION:
#       Code for the Track Model as part of the Pittsburgh Light Rail System
#
##############################################################################


class TrackModel:
    vTrackLayoutFile = 'filename here'
    vRailLines = []
    
    def __init__(self):
        return 42

    # Should parse a given layout file and create the blocks of the rail system accordingly
    def parseLayoutFile(self, pFile):
        return 42

    # Should take the data from the uploaded layout file and create all the block objects
    # required for the rail system and populate their data
    def createTrackLayout(self):
        return 42

    def createRailLine(self, pRailLine):
        return 42

    def createTrackBlock(self, blockparamsgohere):
        return 42

    # INTER-MODULE COMMUNICATION METHODS
    # The Track Model interacts with the Track Controller and the Train Model
    def receiveFromTrackController(self):
        return 42

    def receiveFromTrainModel(self):
        return 42

    def sendRequestToTrackController(self):
        return 42

    def sendRequestToTrainModel(self):
        return 42

    def process(self):
        return 42
