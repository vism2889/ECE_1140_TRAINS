import sys

class Train:
    
    def __init__(self, destinations, suggestedSpeed, authority):
        self.destinations = destinations.copy()
        self.suggestedSpeed = suggestedSpeed
        self.authority = authority
