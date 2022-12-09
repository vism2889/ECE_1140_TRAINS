# Track Model

Track Model description:
    The Track Model sub-system module represents the physical track infrastrucure used for the Pittsburgh Light Rail
Northshore extension.  This module consists of Track Lines, Track Sections, and Track Blocks, and has the functionality to 
display all of the required information about these module elements.

Track Model Example Images:
    Add track model screen shots here

Module Application usage:
    DESCRIPTION of how to use module here:
        - To begin usage of the Track Model one must load a track layout CSV file
        - Once a csv file is loaded a user can select a track line to view track blocks and block information for
        - To trigger a fault for a given block, select the block that you would like to enable a fault for and click one of the fault buttons,
            this will enable a fault in the block inforamton display, the block list, and the the Large main block indicator
    DESCRIPTION of what all module indicators represent

Using the Test UI:
    DESCRIPTION of how to use the test UI here

Directory Details and Code Information:
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
    - Set Beacon correctly
    - Create current block indices for both lines instead of one global indice