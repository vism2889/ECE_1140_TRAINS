#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: LayoutParserTest.py
# DESCRIPTION:
#       Code to test parsing a rail system track layout file and storing the information
#   in variables. 
#
##############################################################################

# IMPORTS
import csv
 
filename = "Track_Layout_PGH_Light_Rail.csv"
fields   = [] # Column Names
rows     = [] # Data Rows / Block Information

print("\n\tPITTSBURGH LIGHT RAIL TRACK-LAYOUT TEST PARSER")
print("\t*****************************************")
with open(filename, 'r') as csvfile:
    print("\tParsing Track Layout File: ", filename)
    csvreader = csv.reader(csvfile)
    fields    = next(csvreader)
    for row in csvreader:
        rows.append(row)
    print("\tFile Parsing Complete\n")
    print("\t\tTotal no. of rows: %d"%(csvreader.line_num))
 
print('\t\tField names are:')
print('\t\t\t->',', '.join(field for field in fields))
print("\t\tThe number of Track Blocks are: ", len(rows))
print("\t\tExample data:")
print("\t\t\t-> Row1 = ", rows[0])

lines = set()
for row in rows:
    lines.add(row[0])
lines = list(lines)
print("\t\tThere are", len(lines), "rail lines in this layout")
print("\t\t\t-> Lines:", lines)

blockCountPerLine = [0]*len(lines)
for row in rows:
    for i in range(len(lines)):
        if row[0] == lines[i]:
            blockCountPerLine[i]+=1

for i in range(len(lines)):
    print("\t\tThe", lines[i], "line has", blockCountPerLine[i], "blocks.")

# Prints out all information for one the first block
print("\t\tExample Block from Row1:",
        "\n\t\t\tLine: ", 
        rows[0][0], 
        "\n\t\t\ttSection: ",
        rows[0][1],
        "\n\t\t\tBlock Number: ",
        rows[0][2],
        "\n\t\t\tBlock Length: ",
        rows[0][3],
        "\n\t\t\tBlock Grade: ",
        rows[0][4],
        "\n\t\t\tSpeed Limit: ",
        rows[0][5],
        "\n\t\t\tInfrastructure: ",
        rows[0][6],
        "\n\t\t\tStation Side: ",
        rows[0][7],
        "\n\t\t\tElevation: ",
        rows[0][8],
        "\n\t\t\tCummulative Elevation: ",
        rows[0][9],
        "\n\t\t\tSeconds to Traverse Block: ",
        rows[0][10])

print("\n\tTEST PARSER FINSIHED")