#!/usr/bin/env python3

import re
import os
import glob
import time
import pathlib
from collections import defaultdict
from datetime import date, datetime, timedelta
from seachfiles4tags import findmulti


# functions
def note_titles():
    for fname in os.listdir(zettelkasten):
        if f in fname:
            print(f'{fname}')
            return fname
      
# def sec_tags():
#     file = open((os.path.join(zettelkasten, fname), "r"))
#     data = file.read()
#     tags = re.findall('#\S\S*', data)         
#     print(tags)   

            
# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")
zettel = "A Proustian View On How to Be a Good Friend 202211140823.md"
note = pathlib.Path("/Users/will/Dropbox/zettelkasten/", zettel)

# file handling
file = open((os.path.join(zettelkasten, zettel)), "r")
data = file.read()

# data processing
tags = re.findall('#\S\S*', data)
links = re.findall("(?<!›)\[\[\d{12}\]\]", data)
source = re.findall('\d{12}', zettel)
mod_time = note.stat().st_ctime

now=datetime.now()
dt_string = now.strftime("%c")

# Print target's tags
for t in tags:
    print(t)
    
# Print target's Links
for l in links:
    f = l[2:-2]
    note_titles() 
    # print(fname)
    # sec_tags()   
    
# Print target's UUID    
print(f"[[{source[0]}]]")
# Print target's modification time
print(f"This zettel was modified at {time.ctime(mod_time)}")
# Print current time
print(f"The current time is {dt_string}.")

tagPattern = "(?<!#)#(?![#, ,'])[0-9,a-z,A-Z]*.|\[\[\D.*\]\]" # Regex pattern to find tags.
targetFile = note_titles() # Directory to search for tags.

# Attempt to find all tags in target's linked files.
for i in findmulti(targetFile, tagPattern):
    if i[1] != []: # This line filters out files that don't have tags.
        unique_list = list(set(i)) # This line removes duplicates.
print(unique_list)

