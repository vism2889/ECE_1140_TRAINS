import csv
import re

class ScheduleParser:

    def __init__(self):
        self.readSchedule = csv.reader

    def loadSchedule(self, scheduleFile, redLineStations, greenLineStations, redLineTrains, greenLineTrains, trainCount):
        with open(scheduleFile) as file:
            self.readSchedule = csv.reader(file)
            foundTrain = False
            trainName = "Train " + str(trainCount)

            for row in self.readSchedule:
                if row[0] == "Red":
                    destination = re.split(': |;', row[1])[1]
                    redLineTrains.addTrain(trainName, redLineStations, 0, 0)
                    foundTrain = True
                    break
                elif row[0] == "Green":
                    destination = (row[1].split(": ")[1])
                    greenLineTrains.addTrain(trainName, greenLineStations, 0, 0)
                    foundTrain = True
                    break

            if not foundTrain:
                return False

            for row in self.readSchedule:
                if row[0] == "Red":
                    destination = re.split(': |;', row[1])[1]
                    redLineTrains.toggleDestination(trainName, destination, False)
                elif row[0] == "Green":
                    destination = (row[1].split(": ")[1])
                    greenLineTrains.toggleDestination(trainName, destination, False)

            return True