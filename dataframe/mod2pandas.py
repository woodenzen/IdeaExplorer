import pandas as pd
import re
import os
import glob
import time
from datetime import datetime
from collections import Counter
from prettytable import PrettyTable
from plistlib import load
from urllib.parse import urlparse

# Function for finding the path to The Archive
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
zettel = "Process And Create New Ideas 202103111214.md"

def add_to_df(zettel):
    # open the file
    with open(os.path.join(zettelkasten, zettel), "r") as f:
        content = f.read()
        word_count = len(content.split())
        # Extract the relevant information from the file using regex
        uuid = re.findall('(?<=›\[\[)\w+(?=\]\])', content)
        # Get the modification time of the file using os.path.getmtime then convert it to a string and format it
        last_mod = os.path.getmtime(TheArchivePath() + zettel)
        # convert the modification time to a datetime object
        last_mod_dt = datetime.fromtimestamp(last_mod)
        last_mod_dt = datetime.strftime(last_mod_dt, "%a %b %d %H:%M:%S %Y")
        # Find all tags in the form of #XXXX
        tags = re.findall(r'#(?!#{1})\S+', content)
        # create a dictionary with the extracted information
        data = {'uuid': [uuid], 'tags': [tags], 'last_mod_dt': [last_mod_dt], 'word_count': [word_count]}
        # create a DataFrame from the dictionary
        df_addition = pd.DataFrame(data, columns = ['uuid', 'tags', 'last_mod_dt', 'word_count'])
    return df_addition

# Also, you should use a loop to iterate through all the markdown files in the directory and call the add_to_df() function for each file, appending the resulting DataFrame to a list. Finally, you can use the pd.concat() function to concatenate all the DataFrames in the list into a single DataFrame, and sort them by the last_mod_dt column.

# pandas merge can check for duplicates and append new rows to the existing DataFrame

# # open the file
# with open(os.path.join(zettelkasten, zettel), "r") as f:
#     content = f.read()
#     word_count = len(content.split())
#     # Extract the relevant information from the file using regex
#     uuid = re.findall('(?<=›\[\[)\w+(?=\]\])', content)
#     # Get the modification time of the file using os.path.getmtime then convert it to a string and format it
#     last_mod = os.path.getmtime(TheArchivePath() + zettel)
#     # convert the modification time to a datetime object
#     last_mod_dt = datetime.fromtimestamp(last_mod)
#     last_mod_dt = datetime.strftime(last_mod_dt, "%a %b %d %H:%M:%S %Y")
#     # Find all tags in the form of #XXXX
#     tags = re.findall(r'#(?!#{1})\S+', content)
#     # create a dictionary with the extracted information
#     data = {'uuid': [uuid], 'tags': [tags], 'last_mod_dt': [last_mod_dt], 'word_count': [word_count]}
#     # create a DataFrame from the dictionary
#     df = pd.DataFrame(data, columns = ['uuid', 'tags', 'last_mod_dt', 'word_count'])

 #   pd.merge(add_to_df("Transition - Lost Years - Wandering 202201200907.md"), how='outer', on='uuid', )

  #  print(add_to_df("Transition - Lost Years - Wandering 202201200907.md"))

# print(df)

# Dataframe Profiling Report
# from pandas_profiling import ProfileReport
# prof=ProfileReport(df)
# prof.to_file(output_file='output.html')


