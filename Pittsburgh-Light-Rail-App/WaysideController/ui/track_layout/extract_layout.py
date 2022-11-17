from copy import deepcopy
import os
import json
import csv

def parseTrackLayout(path, jsonPath):

    REQUIRED_FIELDS = ['Line', 'Section', 'Block Number', 'Infrastructure', "Speed Limit (Km/Hr)"]

    controller = {
        "block-occupancy" : [],
        "switch-state" : [],
        "crossing-state" : [],
        "total-blocks" : 0
    }

    trackLayout = {
        'line' : None,
        'sections' : {}
    }

    IO_CONTROLLERS = []

    UI_CONTROLLERS = []


    ## Opening the csv file with the layout
    with open(path, mode='r') as file:

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
            trackLayout['line'] = 'Red'
        elif "Green Line" in path:
            trackLayout['line'] = 'Green'

        ## Parse through each line in the csv file
        for row in track_layout:
            #####################
            if trackLayout['line'] == None:
                print("Error in parsing layout")
                exit(1)

            if row['Line'] == trackLayout['line']:
                if row['Section'] not in trackLayout['sections']:
                    trackLayout['sections'][row['Section']] = {
                        'blocks'    : [],
                        'switches'  : [],
                        'crossing'  : []
                    }

                ## Populate blocks
                s = trackLayout['sections'][row['Section']]
                s['blocks'].append((row['Block Number'],row['Speed Limit (Km/Hr)'], False))

                ## Populate switches
                if row['Infrastructure'] != None and "SWITCH" in row['Infrastructure']:
                    s['switches'].append(row['Block Number'])

                ## Populate crossing
                if row['Infrastructure'] != None and "CROSSING" in row['Infrastructure']:
                    s['crossing'].append(row['Block Number'])

                ## End of populating trackLayout
            #####################
        ## 
        checkedSections = []
        ## Open json file
        jsonFile = open(jsonPath)
        layout = json.load(jsonFile)

        if trackLayout['line'].lower() not in layout['track']:
            print("Invalid line in json file")
            exit(1)


        VIEW = {
            "block-occupancy" : [],
            "switch-state" : [],
            "crossing-state" : [],
            "total-blocks" : 0
        }

        for c in layout['controllers']:
            controller = {
                'sections' : {}
            }

            ui_controller = {
                    "block-occupancy" : [],
                    "switch-state" : [],
                    "crossing-state" : [],
                    "total-blocks" : 0
                }
            
            for s in c['sections']:
                sec = trackLayout['sections'][s]
                controller['sections'][s] = sec
                
                ## UI info
                ## Block Occupancy
                for block in sec['blocks']:
                    ui_controller['block-occupancy'].append((block[0], s, block[2], block[1]))      
                    ui_controller['total-blocks'] += 1
                    
                    if s not in checkedSections: 
                        VIEW['block-occupancy'].append((block[0], s, block[2], block[1]))      
                        VIEW['total-blocks'] += 1
                
                ## Switch info
                for switch in sec['switches']:
                    ui_controller['switch-state'].append((switch, s, False))
                    if s not in checkedSections: VIEW['switch-state'].append((switch, s, False)) 

                ## Crossing info
                for crossing in sec['crossing']:
                    ui_controller['crossing-state'].append((crossing, s, False))
                    if s not in checkedSections: VIEW['crossing-state'].append((crossing, s, False))

                if s not in checkedSections:
                    checkedSections.append(s)

            UI_CONTROLLERS.append(ui_controller)
            IO_CONTROLLERS.append(controller)

        ## End of opening json file

        ## Close Files
        file.close()
        jsonFile.close()

    print(UI_CONTROLLERS[1])
    return ([VIEW], UI_CONTROLLERS, IO_CONTROLLERS)

if __name__ == '__main__':
    parseTrackLayout("Track Layout & Vehicle Data vF.xlsx - Green Line.csv", "greenline-layout.json")