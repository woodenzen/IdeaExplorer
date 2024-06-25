import glob
import re

def get_subatomic_from_link(link):
    # Escape special characters in the link for regex
    escaped_link = re.escape(link)
    pattern = rf'›\[\[({escaped_link})\]\]'
    subatomic_info = []
    zettelkasten = '/Users/will/Dropbox/zettelkasten'
    
    # List all Markdown files in the directory
    file_names = glob.glob(f'{zettelkasten}/*.md')
    for file_name in file_names:
        with open(file_name, 'r') as f:
            content = f.read()
        # Check if the specific link is in the file using the regex pattern
        if re.search(pattern, content):
            # Adjust the regex to correctly capture the subatomic line
            # Assuming 'Subatomic: ' is followed by the information until the end of the line
            subatomic = re.findall(r'(?<=Subatomic: ).*$', content, flags=re.MULTILINE)
            if subatomic:
                # Store the subatomic information
                subatomic_info.extend(subatomic)
    
    return subatomic_info

# Example usage
if __name__ == "__main__":
    print(get_subatomic_from_link('202305120821'))