import sys
import copy

class Train:

    def __init__(self, destinations, suggestedSpeed, authority):
        self.destinations = copy.deepcopy(destinations)
        self.suggestedSpeed = suggestedSpeed
        self.authority = authority
