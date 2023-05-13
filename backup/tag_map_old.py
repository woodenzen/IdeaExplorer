# Work on tag map for selected files in /Users/will/Dropbox/zettelkasten, include tags in the form of (#tag) output them in the groupings - # in group, # total number in ZK - with a link for a list for each number. `#writing[4,146]` as link to list of 4 in writing and 146 in ZK. 

import os
import re
import sys
import glob
import json
import string
import random
import shutil
import datetime
import subprocess
import collections

def tagmap(zettelgroup):
    """Create a tag map for all files in a ZK. """
    # Get all files in ZK
    # files = glob.glob('/Users/will/Dropbox/zettelkasten/*.md')
    files =  glob.glob(zettelgroup)
    # Create a list of tags
    tags = []
    for file in files:
        # Open each file and read the contents
        with open(file, 'r') as f:
            content = f.read()
            # Find all tags in the file
            tag = re.findall(r'\#\w+', content)
            # Add the tags to the list
            tags += tag
    # Count the number of times each tag appears
    tag_count = collections.Counter(tags)
    # Get the list of unique tags
    tag_list = list(set(tags))
    # print(tag_list)
    # Create a list of tag counts
    tag_counts = []
    for tag in tag_list:
        count = tag_count[tag]
        tag_counts.append(count)
    # print(tag_counts)    
    # Create a list of tag links
    tag_links = []
    for tag in tag_list:
        # link = tag + '[' + str(tag_count[tag]) + ',' + str(len(tags)) + ']'
        link = f'{tag}[{tag_count[tag]}]'
        tag_links.append(link)
    print(files, tag_links)
    return files, tag_links
            
if __name__ == '__main__':
    tagmap('/Users/will/Dropbox/zettelkasten/Romance in Food Writing 202304130824.md')            
