import train

# populate station dictionaries
redLineTrains = []
greenLineTrains = []

def addRedLineTrain(name, destinations):
    redLineTrains.append( train(name, "red"))

    for destination in destinations:
        redLineTrains.
