# Zettelkasten Idea Explorer  
**Script in development**  
**README document in development**  
Think about the Idea Explore as a way to look at note sequences. Sequences that develop an idea.

Here is a [link to the discussion](https://forum.zettelkasten.de/discussion/2565/idea-explorer-an-extension-exclusively-for-the-archive) in the forum.zettelkasten.de forums.


Designed with The Archive, zettelkasting application, in mind. Plain text with wikilinks. 
My ideas ares for this script are modeled after [the public musings of Soren Bjornstad](https://zettelkasten.sorenbjornstad.com/#ImprovementOfDailyWork)  
The Idea Explorer is an idea that can help surface interesting relationships by looking at age and modification times, and the prevalence of incoming and outgoing links. There is likely other relevance that can be "fished out of the idea pond."

![Soren's Idea Explorer](media/Soren'sIdeaExplorer.png)

## Install
- Tested on Python 3.9
- Dependencies are in requirements.txt

## Use
- The script will find your active zettelkasten
- Currently, the script requires Keyboard Maestro. The Keyboard Maestro macros are in the repository. The usual changes are needed in the macros. File locations and triggers.
- In the file `main custom.html` change the location of your copy of `style.css`.
- Make the necessary file location changes in Keyboard Maestro.
- To activate, with The Archive in the foreground, trigger Keyboard Maestro's 'Idea Explorer'. The initial launch will take up to 10 seconds, so be patient. Subsequent triggers will be much shorted. 

## Notes on work to do:

1. Speed, speed, and more speed.
2. I want to prettify the Idea Explorer.
3. Make this not so fussy to install.
4. I want to add to the Idea Explorer an indicator when a note in the proofing inbox.
5. I want to think of some way to present the data that will be pleasing.
6. Change the link weight giving more weight to links to structure notes.
7. Indicate if media is present and the possible link.
8. Create HTML tabs that would allow a group of notes with the same tag ro be opened from the tag cloud tab.


## This is the current status.
- The example is for a note about the spectrum of abstractions when building knowledge.
- Each note is a link.
- Connection type is defined.
- Age is the relative creation time.
- Last Modified and word count are self-explanatory.
- LW stands for 'Link Weight' and this piecce of data is what the Idea Explorer is sorted on. The more links the higher the rating.

 
### Zettel Idea Navigator
Idea Explorer Tab
![Idea Explorer](media/exp%20tab.png)  

Tag Map Tab
![Tag Map](media/tag%20tab.png)  

Subatomic
![Subatomic](media/sub%20tab.png)  
  
## Me
I'm a mediocre programmer.  
I'm a list maker and love note-taking.  
It is something I love doing.  
I may have found a tutor.  
If you can help, please contact me.