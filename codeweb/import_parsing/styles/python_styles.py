from typing import List
from ..import_style import ImportStyle
from ..parsers.python_parsers import parse_import_x, parse_from_y_import_x

python_import_styles: List[ImportStyle] = [
    ImportStyle(extensions=['.py'],
                regex='^import .+', 
                parse_function=parse_import_x),             
    ImportStyle(extensions=['.py'],
                regex='^from .+ import .+', 
                parse_function=parse_from_y_import_x)
]
