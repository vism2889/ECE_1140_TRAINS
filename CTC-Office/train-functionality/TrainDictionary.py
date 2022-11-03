from Train import Train

class TrainDictionary:

    def __init__(self):
        self.trainList = dict()
        self.backLog = dict()

    def addTrain(self, name, destinations, commandedSpeed, authority):
        self.trainList[name] = Train(destinations, commandedSpeed, authority)

    def addScheduledTrain(self, name, destinations, commandedSpeed, authority):
        self.trainList[name] = Train(destinations, commandedSpeed, authority)

    def getCommandedSpeed(self, name):
        return self.trainList[name].commandedSpeed

    def getAuthority(self, name):
        return self.trainList[name].authority

    def getDestinations(self, name):
        return self.trainList[name].destinations

    def toggleDestination(self, name, destination):
        self.trainList[name].destinations[destination] ^= self.trainList[name].destinations[destination]