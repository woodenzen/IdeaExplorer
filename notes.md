1. Make a word cloud of all or a subset of the notes.
   1. could be a separate tab in the custom HTML
   2. word cloud at /Users/will/Dropbox/zettelkasten/Writing/Python/Word Cloud/wcloud.py
2. Simplify the tag cloud.
3. find a way to specify outbound, inbound, or bidirectional for each link.
   1. could be a color in the final custom HTML 

Look at pip install sidetable 
import sidetable
Check out methods
[sidetable · PyPI](https://pypi.org/project/sidetable/#prettyprint)

---
Here's a list of suggested improvements for the code:

- Add docstrings to all functions explaining what the function does, what arguments it takes, and what it returns.
- Replace the defaultdict with a Counter class instance. The code currently has a dictionary of tag counts that needs to be sorted and returned, which can be done more simply using a Counter object.
- Refactor the code to extract common logic into separate functions, as necessary. For example, the logic for finding related records could be put into a separate function, as it's being repeated in explorer() and inbound_uuid().
- Use more descriptive and meaningful variable names, for better readability. For example, zettel is an odd name for a note, so it could be replaced with a more descriptive name such as note.
- Use f-strings instead of the format() method for string formatting.
- The try-except block in tag_cloud() should only catch specific exceptions, such as KeyError or AttributeError.
- Remove commented-out code. This makes the code more readable and less cluttered.
- Refactor the code to make use of os.path.join() instead of string concatenation to build file paths. This makes the code more portable and less error-prone.
