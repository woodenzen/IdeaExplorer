import os
import re
import glob
import pandas as pd
from bs4 import BeautifulSoup

zettelkasten = "/Users/will/Dropbox/zettelkasten"
file_path=zettelkasten, "Character Development Literary Lever 202406170833.md"   
def gather_links(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        print(f"File Path: {file_path}")
    links = [match.group(1) for match in re.finditer(r'\[\[(\w+)\]\]', data)]
    return links

def gather_links_from_links(links, target_file):
    all_links = []
    for link in links:
        markdown_files = glob.glob(f'{zettelkasten}/*{link}.md')
        for file in markdown_files:
            if file == target_file:
                continue
            with open(file, 'r') as f:
                content = f.read()
                second_layer_links = [match.group(1) for match in re.finditer(r'\[\[(\w+)\]\]', content)]
                print(f"Second Layer Links: {second_layer_links}")
                for second_link in second_layer_links:
                    # if second_link == link:
                    #     continue
                    file_name = None  # define file_name here
                    matched_files = glob.glob(f'{zettelkasten}/*{second_link}.md')
                    if matched_files:
                        file_path = matched_files[0]
                        file_name_with_extension = os.path.basename(file_path)
                        file_name, _ = os.path.splitext(file_name_with_extension)
                        print(f"File Name {file_name}")
                    else:
                        print(f"No files matched the pattern {zettelkasten}/*{second_link}.md")
                    if file_name:  # only create zettel if file_name is not None
                        zettel = f"[{file_name}](thearchive://match/›[[{link})"
                        all_links.append({'Title': zettel})
    return all_links

def main(target):
    target_files = glob.glob(f'{zettelkasten}/*{target}.md')
    if not target_files:
        print(f"No files found for target {target}")
        return
    target_file = target_files[0]
    links = gather_links(target_file)
    print(f"Links: {links}")  # print the extracted links
    all_links = gather_links_from_links(links, target_file)
    print(f"All links: {all_links}")  # print the final data
    df = pd.DataFrame(all_links)
    html_table = df.to_html(index=False, escape=False)
    print(html_table)

if __name__ == "__main__":
    # main()
    # main(os.environ["KMVAR_Local_UUID"])
    main("202406072026") # Unentitled to an opinion

