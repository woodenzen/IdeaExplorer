#!/usr/bin/env python3

import re
import os
import glob
import time
import pathlib
from collections import defaultdict
from datetime import date, datetime, timedelta

# functions
def note_title():
    for fname in os.listdir(zettelkasten):
        if f in fname:
            print(f'{fname[:-16]} has the keyword {l}')
    return fname
      
def sec_tags():
    file = open((os.path.join(zettelkasten, fname), "r"))
    data = file.read()
    tags = re.findall('#\S\S*', data)         
    print(tags)   

            
# path to zettelkasten
zettelkasten = pathlib.Path("/Users/will/Dropbox/zettelkasten/")
zettel = "A Proustian View On How to Be a Good Friend  202211140823.md"
note = pathlib.Path("/Users/will/Dropbox/zettelkasten/", zettel)

# file handling
file = open((os.path.join(zettelkasten, zettel)), "r")
data = file.read()

# data processing
tags = re.findall('#\S\S*', data)
links = re.findall("(?<!›)\[\[\d{12}\]\]", data)
source = re.findall('\d{12}', zettel)
mod_time = note.stat().st_ctime


for t in tags:
    print(t)
    
for l in links:
    f = l[2:-2]
    note_title()  
    # print(fname)
    # sec_tags()   
print(f"[[{source[0]}]]")
print(f"This zettel was modified at {time.ctime(mod_time)}")
