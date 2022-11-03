import sys
import pandas as pd
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/train-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/GUI/')
import csv

def readSchedule(scheduleFile):
    readFile = pd.read_excel(scheduleFile)
    readFile.to_csv("schedule.csv",
                    index = None,
                    header = True)

    with open("schedule.csv") as file:
        readSchedule = csv.reader(file)

        for row in readSchedule:
            destinationList = []
            if row[0] == "Red":
                destinationList.append(row[1].split(": ")[1])
                addRedLineScheduledTrain(destinationList, row[2])
            elif row[0] == "Green":
                destinationList.append(row[1].split(": ")[1])
                addGreenLineScheduledTrain(row[1].split(": ")[1], row[2])


            