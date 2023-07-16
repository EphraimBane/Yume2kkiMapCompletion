from bs4 import BeautifulSoup
import argparse
import json
import sys
import os

WRITEVISITED = False
WRITEUNVISITED = True
OUTPUT_ALL = False

# Argument parsing
parser = argparse.ArgumentParser(description="Produces detailed map completion information from a Yume 2kki save file.")
parser.add_argument("savefile", help="The save file to check")
parser.add_argument("--maplist", default="maps.txt", help="A list of accessible maps to use (Default: maps.txt)")
parser.add_argument("--mode", choices=["visited","unvisited","all"], default="unvisited", help="The mode of program operation. (Visited maps, Unvisited maps from the maplist, or all unvisited map IDs.) (Default: unvisited)")
parser.add_argument("-o","--output",default="MAP_COMPLETION.txt", dest="filename", help="The file to output map information to. (Default: MAP_COMPLETION.txt)")
args = parser.parse_args()

INFILE = args.savefile
MAPFILE = args.maplist
OUTPUT_MODE = args.mode
OUTFILE = args.filename

# Convert save to XML + read in data
print("Reading save...")
filename = '.'.join(INFILE.split(".")[:-1])
os.system("lcf2xml.exe --2k "+INFILE)

with open(filename+".esd","r", errors="replace") as f:
    data = f.read()
os.remove(filename+".esd")

savefile = BeautifulSoup(data, "xml")

# Extract the list of visited maps
print("Checking map completion...")
actor = savefile.find('SaveActor', {'id':'0002'})
skills = actor.find('skills')
visitedmaps = [int(n) for n in skills.string.split()]

# Write the map completion list out directly
if OUTPUT_MODE.lower() == "visited":
    with open(OUTFILE,"w") as f:
        f.write("MAP IDS THAT HAVE BEEN VISITED\n")
        f.write("========================================\n")
        f.writelines([str(n)+"\n" for n in visitedmaps])

# Read in/create the maplist
maplist = []
maplist_version = "None"
if OUTPUT_MODE.lower() == "unvisited":
    with open(MAPFILE,"r") as f:
        maplist_version = f.readline().strip()
        maplist = [int(n) for n in f.readlines()]
elif OUTPUT_MODE.lower() == "all":
    for i in range(0,2400):
        maplist.append(i+1)

# Write only map IDs where the mapfile and the map completion differ
if OUTPUT_MODE.lower() == "unvisited" or OUTPUT_MODE.lower() == "all":
    with open(OUTFILE,"w") as f:
        f.write("MAPS IDS THAT HAVE NOT BEEN VISITED\n")
        if OUTPUT_MODE.lower() == "all":
            f.write("This file lists every unregistered map ID, even if they are inaccessible.\n".format(maplist_version))
        else:
            f.write("This maplist was last updated for version {}.\n".format(maplist_version))
        f.writelines([str(n)+"\n" for n in maplist if n not in visitedmaps])

print("Done!")
print("You have visited a total of {} maps.".format(len(visitedmaps)))
