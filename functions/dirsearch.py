#!/usr/bin/env python3

import os
import glob
import pathlib

zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")

# Both of these functions work. The first does some error catching.

# Returns the filename from a search (i) of a directory tree much like grep.
# Limit the directory size. 
def searchforpath(i):
    filePaths = glob.glob(os.path.join(zettelkasten,'**/*{0}*.md'.format(i)), recursive = True)
    fil="No file found."
    if filePaths:
        fil=filePaths[0]
    return fil    

# Function for searching for a file name based on a UUID.     
def getpath(uuid):
    for root, dirs, files in os.walk(zettelkasten):
        for file in files:
            if file.__contains__(uuid):
                return os.path.join(root, file)
        
if __name__ == "__main__":
    path = pathlib.Path("/Users/will/Dropbox/zettelkasten")
    print(searchforpath("Glacial Mice"))    
    print(getpath("202108101600"))

