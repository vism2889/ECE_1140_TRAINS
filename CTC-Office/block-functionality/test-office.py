import sys
from block import *

redLine[0].toggleOccupancy()

for line in redLine:
    print("\nRed Line Block:", line.name)
    print("Occupancy:", line.getOccupancy())
    print("Fault state:", line.getFaultState())
    print("Maintenance state:", line.getMaintenanceState())

for line in blueLine:
    print("\nBlue Line Block:", line.name)
    print("Occupancy:", line.getOccupancy())
    print("Fault state:", line.getFaultState())
    print("Maintenance state:", line.getMaintenanceState())
