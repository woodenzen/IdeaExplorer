#!/usr/bin/env python3
 
import os
import re
import time
import glob
from datetime import datetime
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

# Step 1: Store all files' information in a dictionary

file_info = {}
zk_info = {}

#loop through all files in the zettelkasten with an extension of .md
for file in glob.iglob(zettelkasten+'*.md'):  
    # Extract the file's UUID and title from the file name
    uuid = file[-15:-3]
    title = file.split('/')[-1].split('.')[0][:-13]
        
    # # Birthed time for target from its UUID
    # try:
    #     # Your code that might raise an error
    #     dt = datetime.strptime(uuid, '%Y%m%d%H%M')
    #     birthed = dt.strftime('%c')
    # except ValueError as ve:
    #     # Code to handle the ValueError
    #     # Log the error message or take any other action
    #     print("Caught ValueError:", ve)
    #     print(uuid)
    #     print(file)
    #     print("This file does not have a valid UUID.")
    #     # Continue with the next iteration of the loop
    # continue
    
    # Birthed time for target from its UUID
    dt = datetime.strptime(uuid, '%Y%m%d%H%M')
    birthed = dt.strftime('%c')
   
    # Current time
    now=datetime.now()
    dt_string = now.strftime("%c")

    #####
    # Target file age related math grammar code
    #####

    # Age(a) math and grammar of the target file
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
        
    # Modification time of the file with proper grammar
    mod_time = os.path.getmtime(file) 
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
        last_mod = f'This note was last modified {myears} {mdays} ago'    
        
    else:
        days = mdelta.days
        # total_time = divmod(years, 1)
        mdays=round(days)
        if mdays == 1:
            mdays = str(mdays) + " day"
        else:
            mdays = str(mdays) + " days"
        last_mod = f'This note was last modified {mdays} ago'    
            
    #####
    # Open the file
    #####
    with open((os.path.join(zettelkasten, file)), "r") as f:
        content = f.read()
        wcount = len(content.split())
        
    #####
    # Find all outbound links
    #####
    outbound_links = []
    # Find all links in the form of 12 digits in a row
    link = re.findall(r'\d{12}', content)
    # Store the links in the dictionary
    outbound_links.append(link)
    
    #####
    # Create a dictionary to store the tags for each file
    #####    
    file_tags = []
    # Find all tags in the form of #XXXX preceded by a space
    tags = re.findall(r'#(?!#{1})\S+', content)
    # Store the tags in the dictionary
    file_tags.append(tags)
    # Create each record
    file_info = {"ntitle": title, "fname": file, "cdate": birthed, "age": note_age, "lastmdate": last_mod, "WC": wcount, "outbound": link, "tags": file_tags}
    # Store the record in the dictionary of records with the UUID as the key zk-info[uuid]
    zk_info[uuid] = file_info
    
for key, value in zk_info.items():
    # if value["ntitle"] == "H-University of Idaho":
        print('Record ID:', key)
        print('Record:', value)
   
# How do I print the value of the key 202211171832?
# if zk_info.get("202211171832"):
#     print(zk_info["202211171832"])
   
