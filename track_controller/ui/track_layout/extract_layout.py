import csv
import pandas as pd
import os

REQUIRED_FIELDS = ['Line', 'Section', 'Block Number', 'Infrastructure']
CURR_SECTION = ''
LINE = {
    "block-occupancy" : {
    },
    "switch-state" : {

    },
    "crossing-state" : {

    },
    "total-blocks" : 0
}

class LineConfiguration:
    def __init__(self):

with open("Track Layout & Vehicle Data vF.xlsx - Green Line.csv", mode='r') as file:
        ## Read Header
        track_layout = csv.DictReader(file)

        ## Check for required headers
        for header in REQUIRED_FIELDS:
            if header not in track_layout.fieldnames:
                print(f"{header} not found in file...")
                print('exiting')
                exit(1)

        ## Populate data in to line
        for row in track_layout:
            LINE['total-blocks'] += 1
            if row['Section'] == 'A':
                print(row['Section'])



# with open("Track Layout & Vehicle Data vF.xlsx - Green Line.csv", mode='r') as file:
#     ## Read the CSV file
#     track_layout = pd.read_csv(file)

#     for header in REQUIRED_FIELDS:
#         if header not in track_layout.head(0):
#             print(f"{header} not found in file...")
#             print("exiting")
#             exit(1)

    # for index, row in track_layout.iterrows():
