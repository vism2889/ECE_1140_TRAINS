import train
from train import redLineStations, greenLineStations, train

# populate station dictionaries
redLineTrains = dict()
greenLineTrains = dict()

def addRedLineTrain(destinations, name):
    redLineTrains[name] = train("red")

    for destination in destinations:
        redLineTrains[name].toggleDestination(destination)

def addGreenLineTrain(destinations, name):
    greenLineTrains[name] = train("green")

    for destination in destinations:
        greenLineTrains[name].toggleDestination(destination)


