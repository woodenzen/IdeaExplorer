import os
import re
import glob
import pandas as pd
from subatomicFunction import get_subatomic_from_link


zettelkasten = "/Users/will/Dropbox/zettelkasten"
file_path=zettelkasten, "Character Development Literary Lever 202406170833.md"   
def gather_links(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
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
                for second_link in second_layer_links:
                    # if second_link == link:
                    #     continue
                    file_name = None  # define file_name here
                    matched_files = glob.glob(f'{zettelkasten}/*{second_link}.md')
                    if matched_files:
                        file_path = matched_files[0]
                        file_name_with_extension = os.path.basename(file_path)
                        file_name, _ = os.path.splitext(file_name_with_extension)
                        subatomic_line = get_subatomic_from_link(second_link)[0] if get_subatomic_from_link(second_link) else ''  # Get subatomic line
                        zettel =  f'<a href="thearchive://match/{file_name}"> {file_name[:-13]}</a>'
                        all_links.append({'Title': zettel, 'Subatomic': subatomic_line})
                
    return all_links

def main(target):
    target_files = glob.glob(f'{zettelkasten}/*{target}.md')
    if not target_files:
        # print(f"No files found for target {target}")
        return
    target_file = target_files[0]
    links = gather_links(target_file)
    all_links = gather_links_from_links(links, target_file)
    df = pd.DataFrame(all_links)
    # Assuming 'Title' is the column you want to make unique and sort by
    # Step 1: Drop duplicates based on the 'Title' column
    df_unique = df.drop_duplicates(subset=['Title'])

    # Step 2: Sort the DataFrame by the 'Title' column
    df_sorted = df_unique.sort_values(by=['Subatomic', 'Title'], ascending=[False, True])
    html_table = df_sorted.to_html(index=False, escape=False)
    print(html_table)

if __name__ == "__main__":
    # main()
    main(os.environ["KMVAR_Local_UUID"])
    # main("202303252043") # Unentitled to an opinion

    #TODO - Fix Tag and Subatomic Maps
    #TODO - increase font size
    #TODO - Incorperate link weights and then sort by them.

