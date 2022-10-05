import sys

class train:
    
    def __init__(self, name):
        self.name = name

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


