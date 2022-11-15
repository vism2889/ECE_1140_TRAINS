import sys

class Train:
    
    def __init__(self, destinations, commandedSpeed, authority):
        self.destinations = destinations.copy()
        self.commandedSpeed = commandedSpeed
        self.authority = authority
