#!/usr/local/bin/python3.9 # This is the path to the python3.9 executable on my machine. You may need to change this.

# import time
# startTime = time.time()
 
import os
import re
import time
import glob
import pandas as pd
from datetime import datetime
from plistlib import load
from urllib.parse import urlparse
from collections import Counter
from collections import defaultdict

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
    # Function for outgoing links with note titles
    #####
    def explorer(zettel):
        for key, value in zk_info.items():
            if value["ntitle"] == zettel:
                for i in value["outbound"]:
                    if zk_info.get(i):
                        print(i, zk_info[i]["ntitle"],"\n", zk_info[i]["age"],"\n", zk_info[i]["lastmdate"],"\n", zk_info[i]["WC"], "words")
                        print("This is an outbound link.")
                        print(zk_info[i]["tags"])
                    else:
                        print(i, "This is an intralink.")

    #####
    # Function for tag cloud
    #####
    def tag_cloud(zettel):  # sourcery skip: do-not-use-bare-except
        """
        This function returns a list of tags sorted by the prevalence of their occurrence.

        :param zettel: A string representing a specific record in the `zk_info` dictionary.
        :return: A list of related records to the `zettel`.
        """
        try: # Try to execute the following code block. Some records have empty 'tags' field, so this will throw an error.
            outbound_records = [zk_info[id] for id in zk_info[zettel]['outbound'] if 'outbound' in zk_info[id]]
            tag_count = defaultdict(int)
            for record in outbound_records:
                for tag_list in record['tags']:
                    for tag in tag_list:
                        tag_count[tag] += 1
            sorted_tag_count = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
            for tag, count in sorted_tag_count:
                print(f"{tag} {count}")
                # return tag, count
        except: 
            # Do nothing, just continue execution
            pass
            
    #####
    # Function for inbound links uuids
    #####        
    def inbound_uuid(zettel):
        # sourcery skip: for-append-to-extend, inline-immediately-returned-variable, list-comprehension
        """
        This function returns a list of records related to the `zettel` by checking if the `zettel` is in the 'outbound' field of each record in the `zk_info` dictionary.

        :param zettel: A string representing a specific record in the `zk_info` dictionary.
        :return: A list of related records to the `zettel`.
        """
        related_records = []
        for key, value in zk_info.items():
            # If the record has an 'outbound' field and the `zettel` is in it, and the key is not 'outbound', append the key to the list of related records
            if 'outbound' in value and zettel in value['outbound'] and key != 'outbound':
                related_records.append(key)
        return related_records

    #####
    # Function for labeling links out, in, bidirectional
    #####  
    def label_links(outbound, inbound):
        # This function returns a sorted list of links, to and from the target zettel, with their directionality.
        combined = set(outbound + inbound)
        # set() removes duplicates
        direction = []
        for value in combined:
            if value in outbound and value in inbound:
                direction.append(f"{value} Bilateral")
            elif value in outbound:
                direction.append(f"{value} Outbound")
            elif value in inbound:
                direction.append(f"{value} Inbound")

        direction.sort(key=lambda x: x.split(" ")[0], reverse=True)
        # sort by the first part of the string, which is the UUID, making the list sort with newest dates first
        return direction

    #####
    # Variables
    #####
    zettelkasten = TheArchivePath()
    # zettel = os.environ["KMVAR_UUID"]
    # zettel = "202302121724"

    # Step 1: Store all files' information in a dictionary

    file_info = {}
    zk_info = {}

    #loop through all files in the zettelkasten with an extension of .md
    for file in glob.iglob(f'{zettelkasten}*.md'):  
        # Extract the file's UUID and title from the file name
        uuid = file[-15:-3]
        title = file.split('/')[-1].split('.')[0][:-13]

        # Birthed time for target from its UUID
        dt = datetime.strptime(uuid, '%Y%m%d%H%M')
        birthed = dt.strftime('%a %b %d %Y %I:%M %p')

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
            ayears = f"{str(ayears)} year" if ayears == 1 else f"{str(ayears)} years"
            adays = f"{str(adays)} day" if adays == 1 else f"{str(adays)} days"
            note_age = f'This note has existed for {ayears} and {adays}.'    

        else:
            days = delta.days
            # total_time = divmod(years, 1)
            adays=round(days)
            adays = f"{str(adays)} day" if adays == 1 else f"{str(adays)} days"
            note_age = f'This note has existed for {adays}.'   

        # Modification time of the file with proper grammar
        mod_time = os.path.getmtime(file)
        # How long ago was the last modified (m) - grammar
        timestamp = time.ctime(mod_time)
        timestamp_dt = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %Y")
        mdelta = datetime.now() - timestamp_dt

        # Modified date (m) math and grammar of the target file
        if mdelta.days > 365:
            years = mdelta.days/365
            total_time = divmod(years, 1)
            mdays=round(total_time[1]*365)
            myears=round(total_time[0])
            myears = f"{str(myears)} year" if myears == 1 else f"{str(myears)} years"
            mdays = f"{str(mdays)} day" if mdays == 1 else f"{str(mdays)} days"
            last_mod = f'This note was last modified {myears} {mdays} ago'    

        else:
            days = mdelta.days
            # total_time = divmod(years, 1)
            mdays=round(days)
            mdays = f"{str(mdays)} day" if mdays == 1 else f"{str(mdays)} days"
            last_mod = f'This note was last modified {mdays} ago'    

        #####
        # Open the file
        #####
        with open((os.path.join(zettelkasten, file)), "r") as f:
            content = f.read()
            wcount = len(content.split())

        # Find all links in the form of 12 digits in a row
        link = re.findall(r'\d{12}', content)
        outbound_links = [link]
        # Find all tags in the form of #XXXX preceded by a space
        tags = re.findall(r'#(?!#{1})\S+', content)
        file_tags = [tags]
        # Create each record
        file_info = {"ntitle": title, "fname": file, "cdate": birthed, "age": note_age, "lastmdate": last_mod, "WC": wcount, "outbound": link, "tags": file_tags}
        # Store the record in the dictionary of records with the UUID as the key zk-info[uuid]
        zk_info[uuid] = file_info

    inbound = inbound_uuid(zettel)
    outbound = zk_info[zettel]['outbound']
    direction = label_links(outbound, inbound)
    for item in direction:
        try:
            count=0
            count=zk_info[item.split(" ")[0]]['outbound'] + inbound
            unique_count = sorted(set(count))
            unique_count = len(unique_count)
            LinkWeight = {unique_count-1}
            s=f"""{'★'*1}
{item.split(" ")[0]}
{zk_info[item.split(" ")[0]]['ntitle']}
{item.split(" ")[1]} Connection
{zk_info[item.split(" ")[0]]['cdate']}
{zk_info[item.split(" ")[0]]['age']}
{zk_info[item.split(" ")[0]]['lastmdate']}
Word Count {zk_info[item.split(" ")[0]]['WC']}
{LinkWeight}
{' '*1}
            
            """
            print(s)
                # with open('file.txt', 'a', newline='\n') as f: f.write(data)

        except:
            #Do nothing
            pass
        
    zk_info_df = pd.DataFrame.from_dict(zk_info, orient='index')        
        
    html_table = zk_info_df.to_html(escape=False, formatters=dict(Website=lambda x: '<a href="{}">{}</a>'.format(x, x)))

# Display the HTML table
    #print(html_table)
#print html_table to a file
    print(html_table, file=open("zk_info.html", "w"))
if __name__ == "__main__":
    # main(os.environ["KMVAR_Local_UUID"])
    main("202302280908")
    
# executionTime = (time.time() - startTime)
# print('\n Execution time in seconds: ' + str(executionTime))

