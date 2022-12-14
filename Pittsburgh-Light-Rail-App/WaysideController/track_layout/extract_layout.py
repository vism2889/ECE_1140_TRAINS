import json
import csv
from Track import Track, Block

## Extract controller layout for UI configuration
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
            print(trackLayout['line'].lower())
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

    return ([VIEW], UI_CONTROLLERS, IO_CONTROLLERS)

def generateTrackPath(path, name):
    # with open(path, mode='r', encoding='utf-8-sig') as file:
    with open(path, mode='r') as file:

        ## Return the top of the file
        trackLayout = csv.DictReader(file)
        ## Get the number of lines in the file
        size = 0
        for i in trackLayout:
            size+=1

        ## Create track instance
        track = Track(name, size)

        ## Go back to the top of the file
        file.seek(0)
        trackLayout = csv.DictReader(file)
        yard = Block(0)
        for i in trackLayout:
            block = track.getBlock(int(i['Block']))

            ## Previous = Left, Next = Right
            prev = i['Previous']
            next = i['Next']

            ## previous
            if ';' in prev:
                prev = prev.split(';')
                for j in prev:
                    ## Set previous
                    if int(j) == 0:
                        block.setLeftNode(yard)
                    else:
                        block.setLeftNode(track.getBlock(int(j)))
            else:
                block.setLeftNode(track.getBlock(int(prev)))

            ## next
            if ';' in next:
                next = next.split(';')
                for j in next:
                    ## Set previous
                    if int(j) == 0:
                        block.setRightNode(yard)
                    else:
                        block.setRightNode(track.getBlock(int(j)))
            else:
                block.setRightNode(track.getBlock(int(next)))

            ## Setting switch
            if i['Switch'] != '':
                block.hasSwitch = True
                track.confSwitch(int(i['Switch']), block.id)
                track.setSwitch(int(i['Switch']), True)

    file.close()
    return track


if __name__ == '__main__':

    # fileName = "Track Layout & Vehicle Data vF.xlsx - Green Line.csv"
    # parseTrackLayout(fileName, "greenline-layout.json")

    filename = "Trains Layout - Green Line.csv"
    greenTrack = generateTrackPath(filename, 'green')
    filename = "Trains Layout - Red Line.csv"
    redTrack = generateTrackPath(filename, 'red')

    greenTrack.setSwitch(62)
    greenTrack.getInfo(63)

    greenTrack.getNextBlock(63, 0)

    ## Track simulation for the green line
    # print("Testing track for the greenline(hit enter to continue and 'q' to quit)")
    # prev = 0
    # curr = 63
    # greenTrack.setSwitch(62)
    # key = None

    # while True:
    #     key = input("")
    #     if key == 'q':
    #         break

    #     ## Continue
    #     if key == "":
    #         # print(f'Getting info for block {curr}')
    #         # greenTrack.getInfo(curr)
    #         nb = greenTrack.getNextBlock(curr, prev)
    #         if nb == -1:
    #             print("Error and/or crash!")
    #             exit(0)
    #         print(f'Next block is {nb.id}')
    #         prev = curr
    #         curr = nb.id
    #         continue

    #     ## Set switch
    #     if key != None:
    #         if int(key) > 0:
    #             greenTrack.setSwitch(int(key))
    #             continue

    ## Track simulation for the red line
    print("Testing track for the greenline(hit enter to continue and 'q' to quit)")
    prev = 0
    curr = 9
    while True:
        key = input("")
        if key == 'q':
            break

        ## Continue
        if key == "":
            nb = redTrack.getNextBlock(curr, prev)
            if nb == -1:
                print("Error and/or crash!")
                exit(0)
            print(f'Next block is {nb.id}')
            prev = curr
            curr = nb.id
            continue

        ## Set switch
        if key != None:
            if int(key) > 0:
                redTrack.setSwitch(int(key))
                continue

