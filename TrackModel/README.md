# Track Model

track model description:


FILES:
- LayoutParser.py - loads a track layout from a csv file and prints block information to the terminal
- TrackLine.py    - 
- TrackSection.py -  
- BlockModel.py   - object to hold the information for a single block
- TrackModelUI.py - holds all the logic to generate  a UI and  populate with information


TRACK MODEL TODO:
- Update faults to be block specific
- Heater elements to be block specific
- Add fault indicator in block list to easily see the blocks where faults are present
- Add more unit tests
- create example for sending pickled block objects over TCP connection (for use with win-server)
- create messages for sending to Train  Model
- create messages for receiving  from Wayside Controller