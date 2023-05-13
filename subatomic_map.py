#!/usr/local/bin/python3.9 

# import time
# startTime = time.time()
 
import os
import re
import glob
import pandas as pd
from plistlib import load
from urllib.parse import urlparse
from collections import Counter
 
def main(zettel):
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
    # zettel = "Process And Create New Ideas 202103111214.md"

    #####
    # Idea Explorer Code
    #####
    # Find all links in the form of [[XXXXXXXXXXXXX]]
    file_names = glob.glob(zettelkasten+'*'+zettel+'*.md')
    for file_name in file_names:
        # Open the file
        with open(file_name, 'r') as f:
            content = f.read()
        links = re.findall(r'\[\[\w+\]\]', content)

    # Create a dictionary to store the subatomic for each file
    file_subatomic = {}

    # Iterate through each link looking for files listing subatomic in a dictionary
    for link in links:
        # Get the link without the brackets
        link = link[2:-2]
        # Find all files in the directory that contain the link as a substring
        file_names = glob.glob(f'{zettelkasten}*{link}.md')
        for file_name in file_names:
            # Open the file
            with open(file_name, 'r') as f:
                content = f.read()
            # Find all subatomic fragments
            subatomic = re.findall(r'(?<=Subatomic: ).*(?=\s)', content)
            # Store the file name as a href link in the dictionary
            note_name = file_name[33:-16]
            note_link = f'<a href="thearchive://match/{note_name} {file_name[-15:-3]}">{note_name}</a>'
            # Store the subatomic in the dictionary
            file_subatomic[note_name] = (note_link, ', '.join(subatomic))
 
    # Create a DataFrame from the file_subatomic dictionary
    df = pd.DataFrame.from_dict(file_subatomic, orient='index', columns=['Title', 'Subatomic'])
    # print(df)
    # Reorder the columns
    df = df[['Title', 'Subatomic']]

    #Create HTML and Print html_table to a file
    html_table = df.to_html(index=False, escape=False, formatters=dict(Note=lambda x: '<a href="{}">{}</a>'.format(x[0], x[1])))
    
    # Print the results
    print(html_table)
    # print(df)
if __name__ == "__main__":
    main(os.environ["KMVAR_Local_UUID"])
    # main("202305120821") # Unentitled to an opinion

