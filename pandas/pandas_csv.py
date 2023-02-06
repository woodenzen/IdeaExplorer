import pandas as pd
import re
import os
import ast
import time
from datetime import datetime
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

def extract_data_from_files(file_list, csv_file):
    data = []
    for zettel in file_list:
        with open(os.path.join(zettelkasten, zettel), "r") as f:
            content = f.read()
            #Get the note title from the filename
            title = os.path.basename(zettel).split('.')[0]
            title = title[ :-13]
            # Get the word count of the file
            word_count = len(content.split())
            # Extract the relevant information from the file using regex
            uuid = re.findall('(?<=›\[\[)\w+(?=\]\])', content)
            # Get the modification time of the file using os.path.getmtime then convert it to a string and format it
            last_mod = os.path.getmtime(zettel)
            # convert the modification time to a datetime object
            last_mod_dt = datetime.fromtimestamp(last_mod)
            last_mod_dt = datetime.strftime(last_mod_dt, "%a %b %d %H:%M:%S %Y")
            # Find all links in the form of [[XXXX]]
            links = re.findall(r'\[\[\d{12}\]\]', content)
            # Find all tags in the form of #XXXX
            tags = re.findall(r'#(?!#{1})\S+', content)
            # create a dictionary with the extracted information
            data.append({'title': title, 'uuid': uuid, 'tags': tags, 'links': links, 'last_mod_dt': last_mod_dt, 'word_count': word_count})

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)
    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    # file_list = ["Thinking Rates Are Fixed 202108062019.md", "Thinking that Matters 202005060857.md", "Thinking tool 201901281934.md","Narrative Fallacy 201901031026.md"]

    start_time = time.perf_counter()    
    
    
    # use glob to get a list of all files ending with '.md' in the directory
    file_list = [f for f in os.listdir(zettelkasten) if f.endswith('.md')]
    file_list = [os.path.join(zettelkasten,f) for f in file_list]
    extract_data_from_files(file_list, "data.csv")
    
    data = pd.read_csv("data.csv")
    df = data.copy()
    

    df['tags'] = df['tags'].apply(lambda x: list(set(ast.literal_eval(x))))
    df['links'] = df['links'].apply(lambda x: list(set(ast.literal_eval(x))))
    
    #print only df columns
    print(df['links'])
    # Get the uuid of the first row
    first_row_uuid = df.loc[0, 'uuid']

    # Get the links of the first row
    first_row_links = df.loc[0, 'links']

    # Extract the uuids of the linked rows from the links
    linked_uuids = [link[0].strip('[]') for link in first_row_links]

    # Filter the DataFrame to include the first row and the linked rows
    filtered_df = df[df['uuid'].isin([first_row_uuid]+linked_uuids)]
    print(filtered_df)
    
    end_time = time.perf_counter()
    print(f"The execution time: {end_time - start_time:.8f} seconds")
    print("Done!")