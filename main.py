import re
import os
import glob
import time
from datetime import datetime
from collections import Counter
from prettytable import PrettyTable
from plistlib import load
from urllib.parse import urlparse

#####
# Function for finding the path to The Archive
#####
# Set the active archive path
def TheArchivePath():
#  Variables that ultimately revel The Archive's plist file.
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        pl = load(fp) # load is a special function for use with a plist
        path = urlparse(pl['archiveURL']) # 'archiveURL' is the key that pairs with the zk path
    return (path.path) # path is the part of the path that is formatted for use as a path.

#####
# Variables
#####
zettelkasten = TheArchivePath()
zettel = "Cognitive Bias 201910281718.md"

#####
# Open the file
#####
with open((os.path.join(zettelkasten, zettel)), "r") as f:
    content = f.read()
    
#####
# Timing Math Grammar Code
#####
# Birthed time from UUID
source = re.findall('\d{12}', zettel)
source = source[0]
dt = datetime.strptime(source, '%Y%m%d%H%M')
birthed = dt.strftime('%c')

# Modification time of the target
mod_time = os.path.getmtime(TheArchivePath() + zettel)

# Current time
now=datetime.now()
dt_string = now.strftime("%c")

# Age (a) of the target - grammar
delta = now-dt
if delta.days > 365:
    years = delta.days/365
    total_time = divmod(years, 1)
    adays=round(total_time[1]*365)
    ayears=round(total_time[0])
    if ayears == 1:
        ayears = str(ayears) + " year"
    else:
        ayears = str(ayears) + " years"
    if adays == 1:
        adays = str(adays) + " day"
    else:
        adays = str(adays) + " days"
    note_age = f'This note has existed for {ayears} and {adays}.'    
    
else:
    days = delta.days
    # total_time = divmod(years, 1)
    adays=round(days)
    if adays == 1:
        adays = str(adays) + " day"
    else:
        adays = str(adays) + " days"
    note_age = f'This note has existed for {adays}.'    
    
# How long ago was the last modified (m) - grammar
timestamp = time.ctime(mod_time)
timestamp_dt = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
mdelta = datetime.now() - timestamp_dt

if mdelta.days > 365:
    years = mdelta.days/365
    total_time = divmod(years, 1)
    mdays=round(total_time[1]*365)
    myears=round(total_time[0])
    if myears == 1:
        myears = str(myears) + " year"
    else:
        myears = str(myears) + " years"
    if mdays == 1:
        mdays = str(mdays) + " day"
    else:
        mdays = str(mdays) + " days"
    last_mod = f'This note was last modified {myears} and {mdays} ago.'    
    
else:
    days = mdelta.days
    # total_time = divmod(years, 1)
    mdays=round(days)
    if mdays == 1:
        mdays = str(mdays) + " day"
    else:
        mdays = str(mdays) + " days"
    last_mod = f'This note was last modified {mdays} ago.'    
        
    

#####
# Printing Code
#####
# Rough centering
indent=len(zettel)
# Print target's name
print(f"{str.upper(zettel[:-16]).center(indent)}")
# Print a line of dashes
print(f"{'-'*indent}")
# Print target's age
print(f"{note_age}".center(indent))
# Print target's creation time
print(f"Birthed on {birthed}".center(indent))
# Print how long ago the target was modified
print(f"{last_mod}".center(indent))
# Print target's modification time
print(f"Last modified {time.ctime(mod_time)}".center(indent))
# Print current time
print(f"The current time is {dt_string}.".center(indent))
   
    
#####
# Idea Explorer Code
#####
# Find all links in the form of [[XXXXXXXXXXXXX]]
links = re.findall(r'\[\[\w+\]\]', content)

# Create a dictionary to store the tags for each file
file_tags = {}

# Iterate through each link
for link in links:
    # Get the link without the brackets
    link = link[2:-2]
    # Find all files in the directory that contain the link as a substring
    file_names = glob.glob(zettelkasten+'*'+link+'.md')
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r') as f:
            content = f.read()
        # Find all tags in the form of #XXXX
        tags = re.findall(r'#\w+', content)
        # Store the tags in the dictionary
        file_tags[file_name] = tags

# Print the results
# Create the table
table = PrettyTable()
table.field_names = ["Note Name", "Tags"]

#####
# Modify the tags to be in the format "#tag X" where X is the number of occurrences of the tag
#####
# Original dictionary
tags = file_tags

# Count occurrences of each tag
counts = Counter([tag for values in tags.values() for tag in values])

# Modify each tag to be in the format "#tag X"
modified_tags = {key: [tag + " " + "(" + str(counts[tag]) + ")" for tag in value] for key, value in tags.items()}

# Iterate over the modified_tags dictionary
for file_name, tags in modified_tags.items():
    # Concatenate all the tags using the join function
    tags_str = ", ".join(tags)
    # Add the file name and the concatenated tags to the table
    table.add_row([file_name[33:-15]+"\n"+"[["+file_name[-15:-3]+"]]", tags_str])

# Print the table
print(table)
