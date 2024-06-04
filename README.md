# codeweb
Codebase Visualizer

Provides functionality to scan a codebase (any language) and create a network
graph based on imports. Each file forms a node and is connected to 
any files it imports, or is imported by. Node size corresponds to number of lines
in the file.

Inputs are:
    - path to a codebase
    - list of import styles (regex to detect imports, parsing functions)
    - output file name

Outputs are:
    - html file: interactive network graph of the codebase

For usage example see example.py

![image](https://github.com/tparker48/codeweb/blob/main/screenshot.PNG)
