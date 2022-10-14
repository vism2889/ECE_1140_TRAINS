

class TrackSection:
    def __init__(self, pName):
        self.name      = pName
        self.blocks    = []
        self.stations  = []
        self.switches  = []
        self.crossings = []

    def __str__(self):
        return "Track Section: " + str(self.name)