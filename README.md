# codeweb - Codebase Visualizer

Provides functionality to scan a codebase (any language) and create a interactive network
graph based on imports. Each file forms a node, and each import statement creates
and edge between two nodes. Node size corresponds to number of lines in the file.

Built around pyvis, docs: https://pyvis.readthedocs.io/en/latest/

### Example
```python
  from codeweb.network_builder import NetworkBuilder
  from codeweb.import_parsing.styles.python_styles import python_import_styles
  from pyvis.network import Network

  # Create a new Network with desired settings
  empty_network = Network(directed=True)
  empty_network.repulsion(node_distance=150)

  # Scan project directory and populate network, export to html
  nb = NetworkBuilder(network=empty_network, import_styles=python_import_styles, ignore_external_imports=False)
  populated_network = nb.create_network(project_path='.')
  populated_network.show('example.html', notebook=False)
```

### Scanning Other Languages
Only python is added by default, but this project is organized to make adding new languages
relatively straighforward. To use codeweb on other languages, you just need to use the ImportStyle class (import_parsing/import_style.py).

An ImportStyle provides functionality for detecting import statements and parsing them. 

For examples, see import_parsing/styles/python_styles.py and import_parsing/parsers/python_parsers.py

### Example Output
To tweak graph settings, configure the pyvis Network object before passing it to NetworkBuilder
![image](https://github.com/tparker48/codeweb/blob/main/screenshot.PNG)
