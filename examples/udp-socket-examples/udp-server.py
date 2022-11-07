#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     09/29/2022
# FILENAME: udp-server.py
# DESCRIPTION:
#       Code to demonstrate an example UDP server.
# INSTRUCTIONS FOR USE:
#
##############################################################################


#IMPORTS
import socket, sys

def process():
    UDP_PORT   = 5005 # Port to listen for messages on
    bufferSize = 1024 # should reflect size of messages to be received

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("socket created")
    except socket.error:
        print("failed to create socket. Error code:")
        sys.exit()

    try:
        s.bind(("", UDP_PORT))
        print("bind socket complete")
    except socket.error:
        print("bind failed")
        sys.exit()

    while True:
        message, addr = s.recvfrom(bufferSize)
        message = str(message)
        print(message)

if __name__ == '__main__':
    process()