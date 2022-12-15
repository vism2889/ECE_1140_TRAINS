from Train import Train

class TrainDictionary:

    def __init__(self):
        self.trainList = dict()
        self.backLog = dict()

    def addTrain(self, name, destinations, suggestedSpeed, authority):
        self.trainList[name] = Train(destinations, suggestedSpeed, authority)

    def addScheduledTrain(self, name, destinations, suggestedSpeed, authority):
        self.backLog[name] = Train(destinations, suggestedSpeed, authority)

    def dispatchScheduledTrain(self, time, name):
        self.trainList[name] = self.backLog[time]
        self.backLog.pop(time)

    def setSuggestedSpeed(self, name, TTS, line, scheduled):
        if line == "Green Line":
            distance = 14552.6
        else:
            distance = 5548.2
        velocity = distance/(TTS*60)

        if scheduled:
            self.backLog[name].suggestedSpeed = velocity
        else:
            self.trainList[name].suggestedSpeed = velocity

    def keys(self):
        return self.trainList.keys()

    def backlogs(self):
        return self.backLog.keys()

    def getSuggestedSpeed(self, name):
        return self.trainList[name].suggestedSpeed

    def sendAuthority(self, name, signals):
        destinationList = self.trainList[name].destinations
        stops = []
        for destination in destinationList.keys():
            if destinationList[destination][1]:
                stops.append(destinationList[destination][0])
        signals.ctcAuthoritySignal.emit([name, stops])

    def getDestination(self, name):
        return self.trainList[name].destinations

    def toggleDestination(self, name, destination, scheduled):
        if scheduled:
            self.backLog[name].destinations[destination][1] = not self.backLog[name].destinations[destination][1]
        else:
            self.trainList[name].destinations[destination][1] = not self.trainList[name].destinations[destination][1]