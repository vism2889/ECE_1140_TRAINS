from copy import deepcopy
import os
import csv

def parseTrackLayout(path, size=15):

    REQUIRED_FIELDS = ['Line', 'Section', 'Block Number', 'Infrastructure']
    numBlocksPerController = size

    controller = {
        "block-occupancy" : [],
        "switch-state" : [],
        "crossing-state" : [],
        "total-blocks" : 0
    }

    CONTROLLERS = []
    TOTAL_BLOCKS = 0

    with open(path, mode='r') as file:
        ## Read Header
        getRank = csv.DictReader(file)
        if size == 0:
            numBlocksPerController = sum(1 for row in getRank)

        ## Return to the top of the file - is there a better solution?
        file.seek(0)
        track_layout = csv.DictReader(file)

        ## Check for required headers
        for header in REQUIRED_FIELDS:
            if header not in track_layout.fieldnames:
                print(f"{header} not found in file...")
                print('exiting')
                exit(1)

        ## Populate data in to line
        for row in track_layout:

            TOTAL_BLOCKS += 1
            ## Adding a new controller

            ## Increment the number of blocks assigned
            ## to that controller
            controller['total-blocks'] += 1

            ## populate block-occupancy
            controller['block-occupancy'].append((row['Block Number'], row['Section'], False))

            ## populate switch-state
            if row['Infrastructure'] != None and "SWITCH" in row['Infrastructure']:
                controller['switch-state'].append((row['Block Number'], row['Section'], False))

            ## populate crossing-state
            if row['Infrastructure'] != None and "CROSSING" in row['Infrastructure']:
                controller['crossing-state'].append((row['Block Number'], row['Section'], False))

            if size > 0:
                if TOTAL_BLOCKS % numBlocksPerController == 0:
                    CONTROLLERS.append(deepcopy(controller))
                    controller['block-occupancy'].clear()
                    controller['crossing-state'].clear()
                    controller['switch-state'].clear()
                    controller['total-blocks'] = 0

        CONTROLLERS.append(deepcopy(controller))

        file.close()
    return CONTROLLERS

if __name__ == '__main__':
    print(parseTrackLayout("Track Layout & Vehicle Data vF.xlsx - Green Line.csv"))