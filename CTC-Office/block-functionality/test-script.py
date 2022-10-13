import sys
from block import block

A = block("A")

print("Initial occupancy:", A.getOccupancy())
print("Initial fault state:", A.getFaultState())
print("Initial maintenance state:", A.getMaintenanceState())

A.toggleOccupancy()
A.toggleFaultState()
A.toggleMaintenanceState()

print("\nOne toggle:")
print("New occupancy:", A.getOccupancy())
print("New fault state:", A.getFaultState())
print("New maintenance state:", A.getMaintenanceState())

A.toggleOccupancy()
A.toggleFaultState()
A.toggleMaintenanceState()

print("\nTwo toggles:")
print("New occupancy:", A.getOccupancy())
print("New fault state:", A.getFaultState())
print("New maintenance state:", A.getMaintenanceState())
