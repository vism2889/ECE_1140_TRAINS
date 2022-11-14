from copy import deepcopy
import os
import csv

def parseTrackLayout(path, size=15):

    REQUIRED_FIELDS = ['Line', 'Section', 'Block Number', 'Infrastructure', "Speed Limit (Km/Hr)"]
    numBlocksPerController = size

    controller = {
        "block-occupancy" : [],
        "switch-state" : [],
        "crossing-state" : [],
        "total-blocks" : 0
    }

    layout = {
        'line' : None,
        'sections' : {}
    }

    CONTROLLERS = []
    TOTAL_BLOCKS = 0


    ## Opening the csv file with the layout
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

        if "Red Line" in path:
            layout['line'] = 'Red'
        elif "Green Line" in path:
            layout['line'] = 'Green'

        ##
        for row in track_layout:
            if layout['line'] == None:
                print("Error in parsing layout")
                exit(1)

            if row['Line'] == layout['line']:
                if row['Section'] not in layout['sections']:
                    layout['sections'][row['Section']] = {
                        'blocks'    : [],
                        'switches'  : [],
                        'crossing'  : []
                    }
                ## Populate blocks
                s = layout['sections'][row['Section']]
                s['blocks'].append((row['Block Number'],row['Speed Limit (Km/Hr)'], False))

                ## Populate switches
                if row['Infrastructure'] != None and "SWITCH" in row['Infrastructure']:
                    s['switches'].append(row['Block Number'])

                ## Populate crossing
                if row['Infrastructure'] != None and "CROSSING" in row['Infrastructure']:
                    s['crossing'].append(row['Block Number'])



            #####################



            TOTAL_BLOCKS += 1
            ## Adding a new controller

            ## Increment the number of blocks assigned
            ## to that controller
            controller['total-blocks'] += 1

            ## populate block-occupancy
            controller['block-occupancy'].append((row['Block Number'], row['Section'], False, row['Speed Limit (Km/Hr)']))

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

        if controller['total-blocks'] > 0:
            CONTROLLERS.append(deepcopy(controller))

        file.close()
    return CONTROLLERS

if __name__ == '__main__':
    parseTrackLayout("Track Layout & Vehicle Data vF.xlsx - Green Line.csv")