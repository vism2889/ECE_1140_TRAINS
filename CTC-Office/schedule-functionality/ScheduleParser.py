import re
import pandas as pd
import csv

class ScheduleParser:

    def __init__(self):
        self.readSchedule = csv.reader

    def loadSchedule(self, scheduleFile, redLineStations, greenLineStations, redLineTrains, greenLineTrains):
        self.readFile = pd.read_excel(scheduleFile)
        self.readFile.to_csv("schedule.csv",
                            index = None,
                            header = True)

        with open("schedule.csv") as file:
            self.readSchedule = csv.reader(file)

            for row in self.readSchedule:
                if row[0] == "Red":
                    destination = re.split(': |;', row[1])[1]
                    redLineTrains.addScheduledTrain(row[2], redLineStations, 0, 0)
                    redLineTrains.toggleDestination(row[2], destination, True)
                elif row[0] == "Green":
                    destination = (row[1].split(": ")[1])
                    greenLineTrains.addScheduledTrain(row[2], greenLineStations, 0, 0)
                    redLineTrains.toggleDestination(row[2], destination, True)
