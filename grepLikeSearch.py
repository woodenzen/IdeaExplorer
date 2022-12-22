#!/usr/bin/env python3

import os
import glob
import pathlib

# Returns the filename from a search (i) of a directory tree much like grep.
# Limit the directory size. 
# Be sure to define the `path`

def searchforpath(i):
    filePaths = glob.glob(os.path.join(path,'**/*{0}*.md'.format(i)), recursive = True)
    if filePaths:
        fil=filePaths[0]
    return fil    
        
if __name__ == "__main__":
    path = pathlib.Path("/Users/will/Dropbox/zettelkasten")
    print(searchforpath("Keep Our Utensils"))    
    

