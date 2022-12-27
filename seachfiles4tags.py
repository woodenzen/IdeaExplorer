#!/usr/bin/env python3

import os
import re

# This function looks in a directory (targetDir) of files for the occurrence of tags (tagPattern).

def findmulti(target, pattern, dir="/Users/will/DropBox/zettelkasten/"):
    lst=[]
    with open(dir+target) as f: 
            data=f.read()
            tags=re.findall(pattern, data)
            lst.append(tags)
    return lst 
        
if __name__ == "__main__":
    
    tagPattern= "(?<!#)#(?![#, ,'])[0-9,a-z,A-Z]*.|\[\[\D.*\]\]" # Regex pattern to find tags.
    targetFile="Extract Knowledge From Reading 202201042008.md" # Directory to search for tags.
    
    for i in findmulti(targetFile, tagPattern):
       if i[1] != []: # This line filters out files that don't have tags.
           print(i)

