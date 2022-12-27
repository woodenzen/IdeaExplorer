#!/usr/bin/env python3

import os
import re

# This function looks in a directory (targetDir) of files for the occurrence of tags (tagPattern).

def findmulti(target, pattern):
    lst=[]
    for file in os.listdir(target):
        with open(target + file) as f: 
            data=f.read()
            tags=file, re.findall(pattern, data)
            lst.append(tags)
    return lst 
        
if __name__ == "__main__":
    
    tagPattern= "(?<!#)#(?![#, ,'])[0-9,a-z,A-Z]*.|\[\[\D.*\]\]" # Regex pattern to find tags.
    targetDir="/Users/will/Dropbox/Projects/zettelkasten/testzks/Sample-Zettelkasten-Archive-main/" # Directory to search for tags.
    
    for i in findmulti(targetDir, tagPattern):
       if i[1] != []: # This line filters out files that don't have tags.
           print(i)

