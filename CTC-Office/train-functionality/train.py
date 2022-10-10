import sys

redLineStations = dict()
greenLineStations = dict()

redLineStations["HERRON AVE"] = "no"
redLineStations["SHADYSIDE"] = "no"
redLineStations["SWISSVALE"] = "no"
greenLineStations["PIONEER"] = "no"
greenLineStations["EDGEBROOK"] = "no"
greenLineStations["WHITED"] = "no"

class train:
    
    def __init__(self, name, line):
        self.name = name
        if line == "red":
            self.destinations = redLineStations
        elif line == "green":
            self.destinations = greenLineStations
        else:
            sys.exit("Please input proper line selection (red/green)")

    def getCommandedSpeed(self):
        try:
            self.commandedSpeed
        except:
            return "None"
        return self.commandedSpeed

    def getAuthority(self):
        try:
            self.authority
        except:
            return "None"
        return self.authority

    def setCommandedSpeed(self, commandedSpeed):
        self.commandedSpeed = commandedSpeed

    def setAuthority(self, authority):
        self.authority = authority

    def addDestination(self, station):
        self.destinations.update({station:"yes"})

    def removeDestination(self, station):
        self.destinations.update({station:"no"})

    


