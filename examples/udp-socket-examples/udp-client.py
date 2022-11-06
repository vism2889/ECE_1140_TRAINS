#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     09/29/2022
# FILENAME: udp-client.py
# DESCRIPTION:
#       Code to demonstrate an example UDP client.
# INSTRUCTIONS FOR USE:
#
##############################################################################


#IMPORTS
import socket, sys

def process():
    bufferSize = 1024             # should reflect size of messages to be sent
    UDP_IP     = "192.168.1.158"  # The IP address you would like to send to
    UDP_PORT   = 5005             # The port you would like to sent to
    MESSAGE    = "Hello, World!"  # The message to be sent

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # opens socket
    s.bind(('', UDP_PORT))
    s.setblocking(0) # set to non-blocking so flow of program can continue to execute
    s.sendto(bytes(MESSAGE,"utf-8"),(UDP_IP, UDP_PORT)) # sends note over UDP

if __name__ == '__main__':
    process()