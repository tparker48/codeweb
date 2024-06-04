import re
from typing import List, Callable

class ImportStyle:
    """ ImportStyle encapsulates the logic for two things:
            1. Detecting lines that are imports
            2. Parsing out the list of imported files from those lines

        This abstraction should allow others to use CodeWeb on any programming
        language they want.

        See python_import_styles for example of how to create an ImportStyle.
    """
    def __init__(self, extensions:List[str], regex:str, parse_function:Callable) -> None:
        """ 
        Args:
            - extensions (list): File extensions that this style applies to (eg ['.py']) 
            - regex (str): a regular expression that will match an import/include statement
            - parse_function (Callable): a function that will return the list of imported files
                from any string that matches the regex
        """
        self.extenions = extensions
        self.regex = regex
        self.parse = parse_function
    
    def get_imported_files(self, line) -> List[str]:
        if not re.match(self.regex, line):
            return []
        else:
            return self.parse(line)
        

# Python Import Styles:

def parse_python_standard_import(text):
    imports = []
    text = text[len('import '):]
    words = text.split(',') if ',' in text else [text]
    for word in words:
        imports.append(word.split('.')[-1].strip())
    return imports

def parse_python_from_import(text):
    words = text.split()
    return [words[1].split('.')[-1].strip()]

python_import_styles = [
    ImportStyle(extensions=['.py'],
                regex='^import .+', 
                parse_function=parse_python_standard_import),
    ImportStyle(extensions=['.py'],
                regex='^from .+ import .+', 
                parse_function=parse_python_from_import)
]