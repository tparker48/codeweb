import os
from typing import List
from codeweb.import_parsing.import_style import ImportFile

# Utils ------------------------------------------------------------------------------------
def get_abs_path_from_python_import(source_file_path: str, imported_module: str) -> str:
    if imported_module.startswith('.'):
        while imported_module.startswith('.'):
            imported_module = imported_module[1:]
            source_file_path = os.path.join(source_file_path, '..')
    else:
        source_file_path = os.path.join(source_file_path, '..')
        
    relative_path = '\\'.join(imported_module.split('.'))
    return  os.path.abspath(os.path.join(source_file_path, relative_path))+'.py'

def build_python_import_file(source_file_path: str, imported_module: str) -> ImportFile:
    """ Returns an Import object, given a source file path and imported module.
    """
    abs_path = get_abs_path_from_python_import(source_file_path, imported_module)
    if os.path.exists(abs_path):
        return ImportFile(path=abs_path, is_external=False)
    else:
        return ImportFile(path=imported_module, is_external=True)

# Parsers ------------------------------------------------------------------------------------
def parse_import_x(source_file_path: str, text: str) -> List[ImportFile]:
    text = text[len('import '):]
    import_list = [imported_module.strip() for imported_module in text.split(',')]

    imports = []
    for imported_module in import_list:
        imports.append(build_python_import_file(source_file_path, imported_module))

    return imports

def parse_from_y_import_x(source_file_path: str, text: str) -> List[ImportFile]:
    imported_module = text.split()[1].strip()
    return [build_python_import_file(source_file_path, imported_module)]