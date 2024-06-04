# codeweb - Codebase Visualizer

Provides functionality to scan a codebase (any language) and create a network
graph based on imports. Each file forms a node, and each import statement creates
and edge between two nodes. Node size corresponds to number of lines in the file.

Built around the pyvis, docs: https://pyvis.readthedocs.io/en/latest/

### Example
```python
  from codeweb.network_builder import NetworkBuilder
  from codeweb.import_parsing import python_import_styles
  from pyvis.network import Network

  # Create a new Network with desired settings
  empty_network = Network(directed=True)
  empty_network.repulsion(node_distance=150)

  # Scan project directory and populate network, export to html
  nb = NetworkBuilder(network=empty_network, import_styles=python_import_styles, ignore_external_imports=False)
  populated_network = nb.create_network(project_path='.')
  populated_network.show('example.html', notebook=False)
```

### Scanning other languages
Only python is added by default, but this project is organized to make adding new languages
very straighforward. To use codeweb on other languages, you just need to use the ImportStyle class (import_parsing.py):


```python
# Example: Creating an ImportStyle for python's 'from x.y.z import w' imports:

# To make an ImportStyle, you need three things:

# 1. File Extensions - This list of file extensions this pattern applies to
extensions = ['.py']

# 2. RegEx - A regex string that will match this import style (and only this import style)
regex = '^from .+ import .+'

# 3. Parsing Function - A function returning the list of imported files from regex-matched text
def parse_matched_text(text: str) -> List[str]:
                                                # "from x.y.z import w" 
    imported_name = text.split()[1].strip()     # "x.y.z" 
    module_name = imported_name.split('.')[-1]  # "z"
    return [module_name]                        # ["z"]

# Create the ImportStyle
parse_from_x_import_y = ImportStyle(extensions, regex, parse_matched_text)

# Use the custom ImportStyle
nb = NetworkBuilder(network=empty_network, import_styles=[parse_from_x_import_y])
```


![image](https://github.com/tparker48/codeweb/blob/main/screenshot.PNG)
