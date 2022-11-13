from TrainDictionary import TrainDictionary

myStations = dict()
myStations["SHADYSIDE"] = "no"
myStations["SWISSVALE"] = "no"

myTrains = TrainDictionary()
myTrains.addTrain("Train 1", myStations, 0, 20)

newStationsKeys = myTrains.getDestinations("Train 1").keys()

for key in newStationsKeys:
    print(key)