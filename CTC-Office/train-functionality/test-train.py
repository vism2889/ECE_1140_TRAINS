import sys
from train import train

Train1 = train("red")
Train2 = train("red")

assert(Train1.getAuthority() == "None")
assert(Train1.getCommandedSpeed() == "None")
assert(Train1.destinations.get("SWISSVALE") == "no")

Train1.setAuthority("28")
Train1.setCommandedSpeed("12")
Train1.toggleDestination("SWISSVALE")

assert(Train1.getAuthority() == "28")
assert(Train1.getCommandedSpeed() == "12")
assert(Train1.destinations.get("SWISSVALE") == "yes")
assert(Train2.destinations.get("SWISSVALE") == "no")


print("All tests passed")


