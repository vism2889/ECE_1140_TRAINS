import sys
import pandas as pd
import csv

scheduleFile = (sys.argv[1])
readFile = pd.read_excel(scheduleFile)
readFile.to_csv("schedule.csv",
                index = None,
                header = True)


with open("schedule.csv") as file:
    readSchedule = csv.reader(file)   

    for row in readSchedule:
        print(row)  