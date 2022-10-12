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
    
    def __init__(self, line):
        self.line = line
        self.destinations = dict()
        
        if line == "red":
            for key, value in redLineStations.items():
                self.destinations[key] = value
        elif line == "green":
            for key, value in greenLineStations.items():
                self.destinations[key] = value
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

    def getDestinations(self):
        return self.destinations

    def getLine(self):
        return self.line

    def setCommandedSpeed(self, commandedSpeed):
        self.commandedSpeed = commandedSpeed

    def setAuthority(self, authority):
        self.authority = authority

    def toggleDestination(self, station):
        if self.destinations[station] == "no":
            self.destinations.update({station:"yes"})
        else:
            self.destinations.update({station:"no"})


    


