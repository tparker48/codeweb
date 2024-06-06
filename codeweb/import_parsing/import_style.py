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
            - parse_function (Callable): a function that will return the list of Import objects
                from an import statement and the path of the source file it came from
        """
        self.extenions = extensions
        self.regex = regex
        self.parse = parse_function
    
    def get_imported_files(self, source_file_path, line) -> List[str]:
        if not re.match(self.regex, line):
            return []
        else:
            return self.parse(source_file_path, line)

class ImportFile():
    """ Represents a single imported file. 
    """
    def __init__(self, path: str, is_external:bool) -> None:
        self.path = path
        self.is_external = is_external
