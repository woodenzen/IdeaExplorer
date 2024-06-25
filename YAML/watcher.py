import os
import yaml
from datetime import datetime
from hashlib import md5
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        update_file_modification_time(filename)


MOD_TIME_FILE = ".mod_time.txt"

def update_file_modification_time(filename):
    # Step 1: Get the current modification time of the file
    mtime = os.path.getmtime(filename)

    # Step 2: Read the modification time from the .mod_time.txt file
    try:
        with open(os.path.join(os.path.dirname(filename), MOD_TIME_FILE), "r") as f:
            mod_time_str = f.read().strip()
            mod_time = datetime.fromisoformat(mod_time_str)
    except FileNotFoundError:
        mod_time = datetime.min

    # Step 3: Compare the modification times to see if the file has been modified
    if datetime.fromtimestamp(mtime) > mod_time:
        # Step 4: Read the file and parse its YAML front matter
        with open(filename, "r") as f:
            lines = f.readlines()
            if lines[0].startswith("---"):
                yaml_lines = []
                for i, line in enumerate(lines):
                    if line.startswith("---"):
                        yaml_lines.append(line)
                    else:
                        break
                yaml_str = "".join(yaml_lines[1:-1])
                yaml_dict = yaml.safe_load(yaml_str)
                content_lines = lines[i+1:]
            else:
                yaml_dict = {}
                content_lines = lines

        # Step 5: Convert the modification time to a string in ISO 8601 format
        mod_time_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S")

        # Step 6: Add the modification time to the YAML front matter dictionary
        if yaml_dict is None:
            yaml_dict = {}
        if "modification_time" in yaml_dict:
            yaml_dict["modification_time"] = mod_time_str
        else:
            yaml_dict["modification_time"] = mod_time_str
            yaml_lines.insert(-2, f"modification_time: {mod_time_str}\n")

        # Step 7: Write the updated YAML front matter and file content back to the file
        with open(filename, "w") as f:
            f.write("---\n")
            f.write(yaml.dump(yaml_dict, default_flow_style=False))
            # f.write("---\n")
            f.writelines(content_lines)

        # Step 8: Write the new modification time to the .mod_time.txt file
        with open(os.path.join(os.path.dirname(filename), MOD_TIME_FILE), "w") as f:
            f.write(mod_time_str)



# Example usage:
update_file_modification_time("/Users/will/Dropbox/Projects/zettelkasten/Idea Explorer/YAML/example.md")

if __name__ == '__main__':
    # Watch the current directory for file modifications
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        while True:
            # This loop runs until the program is terminated
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
