Just a slight modification of pprint module: 

-- adding an empty line to the beginning and the end of whatever is being printed, to separate it visually from the text before and after
-- changing some default values: setting the indent to 4, disabling sorting of dict. items and enabling underscore numbers
-- adding some coloring functionality

After installing prprint module in a project's virtualenv you just need to add this line to your script:

from prprint import pprint, clr

Then you can use pprint as usual, and add colors by calling, for example 'clr.RED' before a coloured string and 'clr.END' after it.
Available colors: GREY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN