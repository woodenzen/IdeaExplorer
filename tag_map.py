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

    # Create a dictionary to store the tags for each file
    file_tags = {}

    # Iterate through each link looking for files listing tags in a dictionary
    for link in links:
        # Get the link without the brackets
        link = link[2:-2]
        # Find all files in the directory that contain the link as a substring
        file_names = glob.glob(f'{zettelkasten}*{link}.md')
        for file_name in file_names:
            # Open the file
            with open(file_name, 'r') as f:
                content = f.read()
                tags = re.findall(r'#(?!#{1})\S+', content)
                # Store the file name as a href link in the dictionary
                note_name = file_name[33:-16]
                note_link = f'<a href="thearchive://match/{note_name} {file_name[-15:-3]}">{note_name}</a>'
                # Store the subatomic in the dictionary
                file_tags[note_link] = (note_link, ', '.join(tags))
 

    # Create a DataFrame from the file_tags dictionary
    df = pd.DataFrame.from_dict(file_tags, orient='index', columns=['Title', 'Tags'])

    # Add a column for the file names
    df['Title'] = df.index.str[:]

    # Count occurrences of each tag
    counts = Counter([tag for values in df['Tags'].values for tag in values.split(', ')])

    # Modify each tag to be in the format "#tag X"
    df['Tags'] = df['Tags'].apply(lambda tags: [f"{tag}({str(counts[tag])})" for tag in tags.split(', ')])

    # Concatenate all the tags using the join function
    df['Tags'] = df['Tags'].apply(lambda tags: ", ".join(tags))
    # Reorder the columns
    df = df[['Title', 'Tags']]

        #Create HTML and Print html_table to a file
    html_table = df.to_html(index=False, escape=False, formatters=dict(Note=lambda x: '<a href="{}">{}</a>'.format(x[0], x[1])))
    
        
    # executionTime = (time.time() - startTime)
    # print('\n Execution time in seconds: ' + str(executionTime))
    print(html_table)
if __name__ == "__main__":
    # main(os.environ["KMVAR_Local_UUID"])
    main("202406230717")

# Print the results
# print(df.to_string(index=False))