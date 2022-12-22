#!/usr/bin/env python3

import os
import glob
import pathlib

path = pathlib.Path("/Users/will/Dropbox/zettelkasten")

# Returns the file from a search (i) of a directory tree. 
def searchforpath(i):
    filePaths = glob.glob(os.path.join(path,'./**/*{0}*.md'.format(i)), recursive = True)
    if filePaths:
        print(filePaths[0])
        
if __name__ == "__main__":
    searchforpath("Keep Our Utensils")    
    

