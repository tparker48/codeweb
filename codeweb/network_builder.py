"""
CodeWeb 

Provides functionality to scan a code base (any language) and create a network
graph based on imports. Each file forms a code and is connected to 
any files it imports, or is imported by. Node size corresponds to number of lines
in the file.

Inputs are:
    - path to a codebase
    - list of import styles (regex to detect imports, parsing functions)
    - output file name

Outputs are:
    - html file: interactive network graph of the codebase

"""


import os
from typing import List
from pyvis.network import Network

from .import_parsing import ImportStyle


class SourceFile():
    """ Holds filename and text for a single source file
    """
    def __init__(self, name:str, lines:List[str]) -> None:
        self.name = name.split('.')[0] if '.' in name else name
        self.extension = name.split('.')[1] if '.' else None
        self.full_name = name
        self.lines = lines

    def __len__(self) -> int:
        return len(self.lines)
    

class NetworkBuilder:
    def __init__(self, network: Network, import_styles: List[ImportStyle], ignore_external_imports=True) -> None:
        self.network = network
        self.import_styles = import_styles
        self.ignore_external_imports = ignore_external_imports

    def create_network(self, project_path:str):
        source_files = self.__scan_for_files(project_path)
        return self.__populate_network(source_files)

    def __scan_for_files(self, path: str) -> List[SourceFile]:
        # Create list of all relevant file extensions
        extensions = []
        for import_style in self.import_styles:
            extensions.extend(import_style.extenions)

        # Grab all files with a relevant extension
        source_files = []
        for root, dirs, files in os.walk(path, topdown=False):
            for filename in files:
                if any([filename.endswith(extension) for extension in extensions]):
                    with open(os.path.join(root,filename), 'r') as text:
                        source_files.append(SourceFile(filename, text.readlines()))

        return source_files
    
    def __populate_network(self, source_files:List[SourceFile]) -> List[str]:
        for file in source_files:
            self.__add_source_file(file)
            
        for file in source_files:
            for line in file.lines:
                for import_style in self.import_styles:
                    for imported_file in import_style.get_imported_files(line):
                        is_external = not any([imported_file == dir_file.name for dir_file in source_files])
                        self.__add_import(
                            source_file=file, 
                            imported_file_name=imported_file, 
                            is_external=is_external
                        )

        return self.network
    
    def __add_source_file(self, file:SourceFile) -> None:
        if not self.__node_exists(file.name):
            self.network.add_node(file.name, size=5+round(len(file)**0.6))
    
    def __add_import(self, source_file: SourceFile, imported_file_name: str, is_external: bool):
        if imported_file_name == source_file.name:
            return
        
        if self.ignore_external_imports and is_external:
            return
        
        if is_external:
            self.network.add_node(imported_file_name, size=5, shape='diamond')
        
        self.network.add_edge(imported_file_name, source_file.name)
    
    def __node_exists(self, id:str) -> bool:
            return any([node == id for node in self.network.get_nodes()])
        