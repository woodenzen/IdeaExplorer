#!/usr/bin/env python3

import os
import re

pattern= "(?<!#)#(?![#,'])[0-9,a-z,A-Z]*.|\[\[\D.*\]\]"
targetDir="/Users/will/Dropbox/Projects/zettelkasten/testzks/Sample-Zettelkasten-Archive-main/"

def findmulti(target, pattern):
    for file in os.listdir(target):
        with open(target + file) as f:
            data=f.read()
            print(file, re.findall(pattern, data))
        print(" _____ \n")        
        
if __name__ == "__main__":
    findmulti(targetDir, tagPattern)