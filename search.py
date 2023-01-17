import os
import re
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

def search_for_incoming(UUID):
    files_with_uuid = []
    for root, dirs, files in os.walk(zettelkasten):
        for file in files:
            if os.path.splitext(file)[1] == ".md":
                with open(os.path.join(root, file), 'r') as f: 
                    data=f.read()
                    if re.search(UUID, data):
                        files_with_uuid.append(file)
    return files_with_uuid

if __name__ == "__main__":
    print(search_for_incoming('201910281718'))