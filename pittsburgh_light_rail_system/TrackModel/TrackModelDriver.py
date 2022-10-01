#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     09/30/2022
# FILENAME: TrackModelDriver.py
# DESCRIPTION:
#       Creates a class instance of TrackModel.py and then calls the TrackModel.py functionality
#
##############################################################################

# IMPORTS
from multiprocessing import Process,Pipe
import TrackModel

def main():
    vTrackModel = new TrackModel()
    vTrackModel.re


def send(child_conn):
    msg = "Hello this is Application#2\nYou can call me the Track Controller!\nCalled from Application#1\n"
    child_conn.send(msg)
    child_conn.close()

if __name__ == '__main__':
    print("Hello I am Application#2\nI am the Track Controller\nYou called me directly\n")