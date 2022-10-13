import sys
from train import train

trainList = dict()

trainList["Train 1"] = train(1, "red")
trainList["Train 2"] = train(2, "red")
trainList["Train 3"] = train(3, "red")

print(trainList["Train 1"].getAuthority())

del trainList["Train 2"]

keys = trainList.keys()

for key in keys:
    print(key)

