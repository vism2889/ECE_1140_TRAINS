import sys
from train import train

Train1 = train("Train1", "red")

assert(Train1.getAuthority() == "None")
assert(Train1.getCommandedSpeed() == "None")
assert(Train1.destinations.get("SWISSVALE") == "no")

Train1.setAuthority("28")
Train1.setCommandedSpeed("12")
Train1.addDestination("SWISSVALE")

assert(Train1.getAuthority() == "28")
assert(Train1.getCommandedSpeed() == "12")
assert(Train1.destinations.get("SWISSVALE") == "yes")

Train1.removeDestination("SWISSVALE")
assert(Train1.destinations.get("SWISSVALE") == "no")

print("All tests passed")


