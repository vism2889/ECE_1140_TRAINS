# Track Model


naming and prefix conventions in use:
- p  = a parameter to a class constructor or method.
- v  = a locally scoped variable
- cv = a class variable
- *global variables will be capitolized


track model outline:

rail system = a list of rail line objects
rail line   = a list of BlockModel objects


FILES:
- LayoutParserTest.py - loads a track layout from a csv file and prints block information to the terminal
- InfraParser.py - parses the infrastructure columns of a track layout file for stations and switches
- (TODO) switchParser.py - parses switches for correct block connections (doesnt  need to be a file, but functionality is needed somewhere)
- BlockModel.py - object to hold the information for a single block
- TrackModel.py - holds all the information for a given track (track layout)
- TrackModelUI.py - holds all the logic to generate  a UI and  populate with information