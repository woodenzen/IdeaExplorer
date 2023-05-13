import re
import glob
from datetime import datetime
from collections import Counter
from prettytable import PrettyTable 

#####
# Variables
#####
zettelkasten = "/Users/will/Dropbox/zettelkasten/"
zettel = "Process And Create New Ideas 202103111214.md"

#####
# Idea Explorer Code
#####
# Find all links in the form of [[XXXXXXXXXXXXX]]
file_names = glob.glob(zettelkasten+zettel)
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
        # Find all tags in the form of #XXXX
        tags = re.findall(r'#(?!#{1})\S+', content)
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
modified_tags = {
    key: [f"{tag}({str(counts[tag])})" for tag in value]
    for key, value in tags.items()
}

# Iterate over the modified_tags dictionary
for file_name, tags in modified_tags.items():
    # Concatenate all the tags using the join function
    tags_str = ", ".join(tags)
    # Add the file name and the concatenated tags to the table
    table.add_row([file_name[33:-15]+"\n"+"[["+file_name[-15:-3]+"]]", tags_str])

############################################

# Print the table
print(table.get_string(title="Idea Explorer"))
