import train
from train import redLineStations, greenLineStations

# populate station dictionaries
redLineTrains = dict()
greenLineTrains = dict()

totalRedLineTrains = 0
totalGreenLineTrains = 0

def addRedLineTrain(destinations):
    trainName = "Train " + str(totalRedLineTrains+1)
    redLineTrains[trainName] = train("red")

    for destination in destinations:
        redLineTrains[trainName].addDestination(destination)
    
    totalRedLineTrains += 1

def addGreenLineTrain(destinations):
    trainName = "Train " + str(totalGreenLineTrains+1)
    greenLineTrains[trainName] = train("red")

    for destination in destinations:
        greenLineTrains[trainName].addDestination(destination)

    totalGreenLineTrains += 1

