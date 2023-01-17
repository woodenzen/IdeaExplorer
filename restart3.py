import re
import os
import glob
import time
from datetime import datetime, timedelta
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
zettel = "G-Developing Craft 202107122044.md"

#####
# Open the file
#####
with open((os.path.join(zettelkasten, zettel)), "r") as f:
    content = f.read()
    
#####
# Timing Code
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

# Age of the target
delta = now-dt
if delta.days > 365:
    years = delta.days/365
    total_time = divmod(years, 1)
    age_days=round(total_time[1]*365)
    age_years=round(total_time[0])
    if age_years == 1:
        age_years = str(age_years) + " year"
    else:
        age_years = str(age_years) + " years"
    if age_days == 1:
        age_days = str(age_days) + " day"
    else:
        age_days = str(age_days) + " days"
    note_age = f'This note is {age_years} and {age_days} old.'    
    
else:
    days = delta.days
    # total_time = divmod(years, 1)
    age_days=round(days)
    if age_days == 1:
        age_days = str(age_days) + " day"
    else:
        age_days = str(age_days) + " days"
    note_age = f'This note is {age_days} old.'    
    
    
    
# Rough centering
indent=len(zettel)

#####
# Printing Code
#####
# Print target's name
print(f"{str.upper(zettel[:-16]).center(indent)}")
# Print a line of dashes
print(f"{'-'*indent}")
# Print target's creation time
print(f"Birthed on {birthed}".center(indent))
# Print target's age
print(f"{note_age}".center(indent))
# Print target's modification time
print(f"Last modified {time.ctime(mod_time)}".center(indent))
# Print current time
print(f"Current time is {dt_string}.".center(indent))
# How much time between now and birthed

    
    
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

# Iterate over the file_tags dictionary
for file_name, tags in file_tags.items():
    # Concatenate all the tags using the join function
    tags_str = ", ".join(tags)
    # Add the file name and the concatenated tags to the table
    table.add_row([file_name[33:-15], tags_str])

# Print the table
print(table)