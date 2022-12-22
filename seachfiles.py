#!/usr/bin/env python3

import os
import glob
import pathlib
import re
this is a test.

pattern= "(?<!#)#(?![#,'])[0-9,a-z,A-Z]*.|\[\[\D.*\]\]"
targetDir="/Users/will/Dropbox/Projects/zettelkasten/testzks/Sample-Zettelkasten-Archive-main/"

for file in os.listdir(targetDir):
    with open(targetDir + file) as f:
        data=f.read()
        try:
            print(file, re.findall(pattern, data))
        except:
            print("Search not found.")
    print(" _____ \n")        
        