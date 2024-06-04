# codeweb - Codebase Visualizer

Provides functionality to scan a codebase (any language) and create a network
graph based on imports. Each file forms a node, and each import statement creates
and edge between two nodes. Node size corresponds to number of lines in the file.

Built around the pyvis, docs: https://pyvis.readthedocs.io/en/latest/

### Example
```
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


```
  # Example ImportStyle for Python - 'from X.Y.Z import W':

    # 1. list of extensions that this rule should apply to
    extensions = ['.py']

    # 2. a regex that will match this import type
    regex = '^from .+ import .+'

    # 3. a function that can pull the imported file names out of the matched text
    def parse_from_style_import(text: str) -> List[str]:
        words = text.split()
        return [words[1].split('.')[-1].strip()]

    # Create the import style like so:
    my_import_style = ImportStyle(extensions, regex, parse_from_style_import)

    When creating the NetworkBuilder, pass it a list of any number of ImportStyle:
    nb = NetworkBuilder(some_network, import_styles=[my_impor_style])
]
```


![image](https://github.com/tparker48/codeweb/blob/main/screenshot.PNG)
