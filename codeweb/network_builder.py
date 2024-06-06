"""
CodeWeb - Codebase Visualizer

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

"""
import os
from typing import List
from pyvis.network import Network

from .import_parsing.import_style import ImportStyle, ImportFile


class SourceFile():
    """ Holds filename and text for a single source file
    """
    def __init__(self, path:str, name:str, lines:List[str]) -> None:
        self.path = os.path.abspath(os.path.join(path, name))
        self.name = name.split('.')[0]
        self.extension = name.split('.')[1] if '.' else None
        self.lines = lines

    def __len__(self) -> int:
        return len(self.lines)

class NetworkBuilder:
    def __init__(self, network: Network, import_styles: List[ImportStyle], ignore_external_imports=True) -> None:
        self.network = network
        self.import_styles = import_styles
        self.ignore_external_imports = ignore_external_imports

    def create_network(self, project_path:str):
        self.project_abs_path = os.path.abspath(project_path)
        self.project_path_stub = self.project_abs_path.split(project_path)[0]
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
                        source_files.append(SourceFile(root, filename, text.readlines()))

        return source_files

    def __populate_network(self, source_files:List[SourceFile]) -> List[str]:
        for file in source_files:
            self.__add_source_file(file)
        
        for file in source_files:
            for line in file.lines:
                for import_style in self.import_styles:
                    for import_file in import_style.get_imported_files(file.path, line):
                        self.__add_import(
                            source_file=file, 
                            import_file=import_file
                        )

        return self.network
    
    def __add_source_file(self, file:SourceFile) -> None:
        node_name = self.__get_node_name_from_absolute_path(file.path)

        if not self.__node_exists(node_name):
            self.network.add_node(node_name, size=5+round(len(file)**0.6))
    
    def __add_import(self, source_file: SourceFile, import_file: ImportFile) -> None:
        if import_file.is_external and self.ignore_external_imports:
            return
        
        source_node_name = self.__get_node_name_from_absolute_path(source_file.path)
        if import_file.is_external:
            import_node_name = import_file.path
        else:
            import_node_name = self.__get_node_name_from_absolute_path(import_file.path)
            
        if import_file.path != source_file.path:
            self.network.add_node(import_node_name, size=5, shape='diamond')
            self.network.add_edge(import_node_name, source_node_name)
    
    def __get_node_name_from_absolute_path(self, abs_path: str) -> str:
        return abs_path.split(self.project_path_stub)[1]

    def __node_exists(self, id:str) -> bool:
            return any([node == id for node in self.network.get_nodes()])
        