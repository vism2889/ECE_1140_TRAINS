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
- layoutParserTest.py - loads a track layout from a csv file and prints block information to the terminal
- infraParser.py - parses the infrastructure columns of a track layout file for stations and switches
- (TODO) switchParser.py - parses switches for correct block connections 
- BlockModel.py - object to hold the information for a single block
- TrackModel.py - holds all the information for a given track (track layout)