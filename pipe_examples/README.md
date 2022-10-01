### This contains example code to reference when setting up a pipe to connect processes between python applications.
### This will probably be used for inter-communication between all software modules.

## INSTRUCTIONS FOR USE
The inter-communication between modules is started by executing `python3 application1.py`.  This will call on a process called `send()` in each of the other `applicationN.py` files for the N applications in this folder.

Each application can also be called directly `python3 applicationN.py` for eeach of the N applications in this folder.