# Track Model

track model description:


Directory Details:
- Layout-Files: 
    - Holds Track Layout CSV files
- Parsers:
    - Holds Parsers used to parse the Track Layout files
- Track-System-Models:
    - TrackLine.py              : Represents a physical track line that has individual track sections
    - TrackSection.py           : Represents a physical track section that has individual track blocks
    - BlockModel.py             : Represents a physical track block
- UI:
    - launchComms.py            : Launches the TrackModelApp and signal communication tests
    - occupancySignalSender.py  : Testing script to send occupancy signal communication
    - TrackModelApp.py          : Main TrackModel user interface / application
- Unit-Tests:
    - BlockModel_UnitTest.py
    - LayoutParser_UnitTest.py
    - TrackLine_UnitTest.py
    - TrackModel_UnitTest.py
    - TrackSection_UnitTest.py



TRACK MODEL TODO:
- Update faults to be block specific
- Heater elements to be block specific
- Add fault indicator in block list to easily see the blocks where faults are present
- Add more unit tests
- create example for sending pickled block objects over TCP connection (for use with win-server)
- create messages for sending to Train  Model
- create messages for receiving  from Wayside Controller