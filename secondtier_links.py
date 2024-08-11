import os
import glob
import pandas as pd
import re
from multiprocessing import Pool
from functools import wraps
import time

zettelkasten = '/Users/will/Dropbox/zettelkasten'  # Ensure this path is correct

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def gather_links(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    links = {match.group(1) for match in re.finditer(r'\[\[(\w+)\]\]', data)}
    return links

def find_inbound_links(target_link):
    inbound_files = []
    markdown_files = glob.glob(f'{zettelkasten}/*.md')
    for file in markdown_files:
        with open(file, 'r') as f:
            content = f.read()
            if re.search(rf'\[\[{target_link}\]\]', content):
                inbound_files.append(file)
    return inbound_files

def process_file(file):
    with open(file, 'r') as f:
        content = f.read()
    second_layer_links = {match.group(1) for match in re.finditer(r'\[\[(\w+)\]\]', content)}
    return file, second_layer_links

# @timing_decorator
def gather_links_from_links(links, target_file):
    all_links = []
    markdown_files = set()
    for link in links:
        markdown_files.update(glob.glob(f'{zettelkasten}/*{link}.md'))
        markdown_files.update(find_inbound_links(link))

    markdown_files.discard(target_file)  # Remove target file from the set

    with Pool() as pool:
        results = pool.map(process_file, markdown_files)

    for file, second_layer_links in results:
        for second_link in second_layer_links:
            matched_files = glob.glob(f'{zettelkasten}/*{second_link}.md')
            if matched_files:
                file_path = matched_files[0]
                file_name_with_extension = os.path.basename(file_path)
                file_name, _ = os.path.splitext(file_name_with_extension)
                subatomic_line = get_subatomic_from_link(second_link)[0] if get_subatomic_from_link(second_link) else ''
                zettel = f'<a href="thearchive://match/{file_name}"> {file_name[:-13]}</a>'
                all_links.append({'Title': zettel, 'Subatomic': subatomic_line})
    return all_links

# @timing_decorator
def get_subatomic_from_link(link):
    escaped_link = re.escape(link)
    pattern = rf'›\[\[({escaped_link})\]\]'
    subatomic_info = []
    file_names = glob.glob(f'{zettelkasten}/*.md')
    for file_name in file_names:
        with open(file_name, 'r') as f:
            content = f.read()
        if re.search(pattern, content):
            subatomic = re.findall(r'(?<=Subatomic: ).*$', content, flags=re.MULTILINE)
            if subatomic:
                subatomic_info.extend(subatomic)
    return subatomic_info

# @timing_decorator
def main(target):
    target_files = glob.glob(f'{zettelkasten}/*{target}.md')
    if not target_files:
        print(f"No files found for target {target}")
        return
    target_file = target_files[0]
    links = gather_links(target_file)

    all_links = gather_links_from_links(links, target_file)

    df = pd.DataFrame(all_links)
    df_unique = df.drop_duplicates(subset=['Title'])

    if 'Subatomic' in df_unique.columns and 'Title' in df_unique.columns:
        df_sorted = df_unique.sort_values(by=['Subatomic', 'Title'], ascending=[False, True])
    else:
        missing_columns = [col for col in ['Subatomic', 'Title'] if col not in df_unique.columns]
        print(f"Missing columns in DataFrame: {missing_columns}")
        if 'Title' in df_unique.columns:
            df_sorted = df_unique.sort_values(by='Title', ascending=True)
        else:
            df_sorted = df_unique  # No sorting if 'Title' is also missing

    html_table = df_sorted.to_html(index=False, escape=False)
    print(html_table)


if __name__ == "__main__":
    # main()
    main(os.environ["KMVAR_Local_UUID"])
    # main("202303252043") # Unentitled to an opinion

    #TODO - Fix Tag and Subatomic Maps
    #TODO - increase font size
    #TODO - Incorperate link weights and then sort by them.