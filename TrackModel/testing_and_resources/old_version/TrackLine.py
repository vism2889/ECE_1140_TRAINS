



class TrackLine:
    def __init__(self, pName):
        self.name      = pName
        self.sections  = []
        self.blocks    = []
        self.sectionNames = []
        self.stations  = []
        self.switches  = []
        self.crossings = []

    def __str__(self):
        return "Track Line: " + str(self.name)