# Sort-Cv-By-City

## Description
This script manages .docx and .pdf files and sorts them into different folders by region of Israeli cities.
any file inside the "Sort-Cv-By-City" folder will be classified into 1 out of 7 regions and move the file into "Sort-Cv-By-City/'region". 
it works by searching for the correct string, therefore files containg an image and no strings might cause unexpected behavior.
files that are failed to be classified are not moved.

### Prerequisites
Python 3.6+
python-docx library
PyPDF2 library

### Installing Steps
download python 3.6+ https://www.python.org/downloads/ 
in the terminal type:
pip install python-docx PyPDF2

