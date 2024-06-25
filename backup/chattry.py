import os

# Step 1: Store all files' information in a dictionary
file_info = {}
for file in os.listdir("/Users/will/Dropbox/zettelkasten"):
    # Extract the file's UUID, creation date, and tags
    uuid = file[-15:12]
    creation_date = os.path.getctime("/Users/will/Dropbox/zettelkasten/"+file)
    with open("/Users/will/Dropbox/zettelkasten/"+file, "r") as f:
        content = f.read()
    tags = [tag.strip() for tag in content.split("#") if tag.startswith(" #")]
    file_info[uuid] = (file, creation_date, tags, os.path.getmtime("/Users/will/Dropbox/zettelkasten/"+file))

# Step 2: Read each file and parse its contents
for file in os.listdir("/Users/will/Dropbox/zettelkasten"):
    with open("/Users/will/Dropbox/zettelkasten/"+file, "r") as f:
        content = f.read()
    links = [link.strip("[]") for link in content.split("[[") if link.endswith("]]")]
    link_info = []
    # Step 3: Look up each link's information in the dictionary
    for link in links:
        link_uuid = link.split("_")[0]
        link_info.append(file_info[link_uuid])
    # Step 4: Convert the list of link information into a table
    print("Links in", file)
    print("Name\t\tUUID\t\tCreation Date\t\tModification Date\t\tTags")
    for info in link_info:
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(info[0], info[0].split("_")[0], info[1], info[3], ", ".join(info[2])))
