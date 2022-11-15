from Train import Train

class TrainDictionary:

    def __init__(self):
        self.trainList = dict()
        self.backLog = dict()

    def addTrain(self, name, destinations, commandedSpeed, authority):
        self.trainList[name] = Train(destinations, commandedSpeed, authority)

    def addScheduledTrain(self, name, destinations, commandedSpeed, authority):
        self.backLog[name] = Train(destinations, commandedSpeed, authority)

    def dispatchScheduledTrain(self, name):
        self.trainList[name] = self.backLog[name]
        self.backLog.pop(name)

    def keys(self):
        return self.trainList.keys()

    def backlogs(self):
        return self.backLog.keys()

    def getCommandedSpeed(self, name):
        return self.trainList[name].commandedSpeed

    def getAuthority(self, name):
        return self.trainList[name].authority

    def getDestination(self, name):
        return self.trainList[name].destinations

    def toggleDestination(self, name, destination, scheduled):
        if scheduled:
            self.backLog[name].destinations[destination][0] = not self.backLog[name].destinations[destination][0]
        else:
            self.trainList[name].destinations[destination][0] = not self.trainList[name].destinations[destination][0]