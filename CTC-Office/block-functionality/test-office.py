import sys
from lines import redLine, redLineLookup

for line in redLine:
    print("\nRed Line Block:", line.name)
    print("Occupancy:", line.getOccupancy())
    print("Fault state:", line.getFaultState())
    print("Maintenance state:", line.getMaintenanceState())

